from app.utils.bot_common import ctx_id2event
import asyncio
import pickle

from loguru import logger
from nonebot import CommandSession, CommandGroup
from nonebot import permission as perm, get_bot
from app.config import MyConfig
from nonebot.command import call_command
from nonebot.command.argfilter import extractors, validators, controllers
from app.libs.scheduler import scheduler
from apscheduler.triggers.interval import IntervalTrigger  # 间隔触发器
from app.models.subcribe import SubContent, SubUser
from app.utils.rss import get_rss_info, diff, mk_msg_content
from app.utils.bot_common import send_msgs
from .rsshub_wrapper import get_rss_list, make_url

__plugin_name__ = "通知"

PLUGIN_NAME = "subscribe"

cg = CommandGroup(
    "subscribe", permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
)


@cg.command("subscribe", aliases=["订阅", "添加订阅", "新增订阅", "新建订阅"], only_to_me=False)
async def subscribe(session: CommandSession):
    message = session.get(
        "message",
        prompt=f"你想订阅什么内容呢，请输入序号？（可输入 `取消、不` 等取消）：\n{get_rss_list()}",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )

    urls = make_url(int(message))
    await asyncio.wait(
        [
            call_command(
                session.bot,
                session.ctx,
                ("rss", "add"),
                args={"url": url},
                disable_interaction=True,
            )
            for url in urls
        ]
    )


@subscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


@cg.command("show", aliases=["查看订阅", "我的订阅"], only_to_me=False)
async def _(session: CommandSession):
    subs = session.state.get("subs") or await SubUser.get_user_subs(session.event)

    if not subs:
        session.finish(f"你还没有订阅任何内容哦")

    for i, sub in enumerate(subs):
        await session.send(format_subscription(i + 1, sub))
        await asyncio.sleep(0.2)
    session.finish(f"以上是所有的 {len(subs)} 个订阅")


@cg.command("unsubscribe", aliases=["取消订阅", "停止订阅", "关闭订阅", "删除订阅"], only_to_me=False)
async def unsubscribe(session: CommandSession):
    subs = await SubUser.get_user_subs(session.event)
    index = session.state.get("index")
    if index is None:
        session.state["subs"] = subs
        await call_command(
            session.bot,
            session.ctx,
            ("subscribe", "show"),
            args={"subs": subs},
            disable_interaction=True,
        )

        if not subs:
            session.finish()

        index = session.get(
            "index",
            prompt="你想取消哪一个订阅呢？（请发送序号）",
            arg_filters=[
                extractors.extract_text,
                controllers.handle_cancellation(session),
                validators.ensure_true(str.isdigit, "请输入序号哦～"),
                int,
            ],
        )

    index = index - 1
    if not (0 <= index < len(subs)):
        session.finish("没有找到你输入的序号哦")

    sub = subs[index]

    try:
        await SubUser.remove_sub(session.event, sub.link)
        await session.send("取消订阅成功")
    except Exception as e:
        logger.exception(e)
        await session.send("出了点问题，请稍后再试吧")


def format_subscription(index: int, sub) -> str:
    return f"序号：{index}\n" f"订阅名称：" f"{sub.sub_content.name}\n" f"订阅链接：" f"{sub.link}"


@scheduler.scheduled_job(
    IntervalTrigger(seconds=MyConfig.SUBSCIBE_INTERVAL, jitter=60),
    id="push_school_notice",
)
async def push():
    logger.info("开始检查RSS更新")
    all_subs = await SubContent.query.gino.all()
    await asyncio.wait([check_update(sub) for sub in all_subs])


async def check_update(sub):
    users = await SubUser.get_user(sub.link)
    event_list = [ctx_id2event(user.ctx_id) for user in users]
    logger.info("检查" + sub.name + "更新")
    logger.info(sub.name + "的用户们：" + str(users))
    if not users:
        return
    content = await get_rss_info(sub.link)
    old_content = pickle.loads(sub.content)
    diffs = diff(content, old_content)
    print("diffs: ", diffs)
    msgs = mk_msg_content(content, diffs)
    print("msgs: ", msgs)

    await asyncio.wait([send_msgs(event, msgs) for event in event_list])
    await SubContent.add_or_update(sub.link, sub.name, pickle.dumps(content))
