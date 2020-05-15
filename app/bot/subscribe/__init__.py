import asyncio
from typing import Optional

from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from nonebot import CommandGroup, CommandSession
from nonebot import permission as perm
from nonebot.command import call_command
from nonebot.command.argfilter import controllers, extractors, validators

from app.config import MyConfig
from app.libs.scheduler import scheduler
from app.models.subcribe import SubContent, SubUser

from .school_notice import get_rss_list, make_url

__plugin_name__ = "订阅"
__plugin_short_description__ = "订阅 通知/成绩/考试 等"
__plugin_usage__ = r"""添加订阅：
    - 订阅
    - 添加订阅
    - 新建订阅
    - subscribe
    然后会提示输入序号，你也可以直接在后面加上序号，如：
        - 订阅 1
        - 订阅 0
查看订阅：
    - 查看订阅
    - subscribe show

移除订阅：
    - 移除订阅
    - 取消订阅
    - 停止订阅
    - 删除订阅
    - subscribe rm
    然后会提示输入序号，你也可以直接在后面加上序号，如：
        - 移除订阅 1
        - 移除订阅 all
""".strip()
PLUGIN_NAME = "subscribe"

cg = CommandGroup(
    PLUGIN_NAME, permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
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


@cg.command("rm", aliases=["取消订阅", "停止订阅", "关闭订阅", "删除订阅", "移除订阅"], only_to_me=False)
async def unsubscribe(session: CommandSession):
    subs = await SubUser.get_user_subs(session.event)
    index: Optional[str] = session.state.get("index")
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
            prompt="你想取消哪一个订阅呢？（请发送序号，或者 `all`/`所有`）",
            arg_filters=[
                extractors.extract_text,
                controllers.handle_cancellation(session),
                validators.ensure_true(str.isdigit, "请输入序号哦～"),
            ],
        )

    async def rm_sub(sub):
        try:
            await SubUser.remove_sub(session.event, sub.link)
            await session.send(f"{sub.sub_content.name} 取消订阅成功")
        except Exception as e:
            logger.exception(e)
            await session.send("出了点问题，请稍后再试吧")

    if index.isdigit():
        idx = int(index)  # type: ignore
        idx = idx - 1
        if not (0 <= idx < len(subs)):
            session.finish("没有找到你输入的序号哦")

        sub = subs[idx]
        await rm_sub(sub)
        return

    if index in ("all", "所有"):
        await asyncio.wait([rm_sub(sub) for sub in subs])


@unsubscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["index"] = session.current_arg


def format_subscription(index: int, sub) -> str:
    return f"序号：{index}\n" f"订阅名称：" f"{sub.sub_content.name}\n" f"订阅链接：" f"{sub.link}"


@scheduler.scheduled_job(
    IntervalTrigger(seconds=MyConfig.SUBSCIBE_INTERVAL, jitter=60),
    id="push_school_notice",
)
async def push():
    await SubContent.check_update()
