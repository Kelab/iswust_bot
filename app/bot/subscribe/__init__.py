import asyncio
from typing import Optional

from loguru import logger
from nonebot import CommandGroup, CommandSession
from nonebot import permission as perm
from nonebot.command import call_command
from nonebot.command.argfilter import controllers, extractors, validators


from app.services.subscribe.school_notice import get_rss_list
from app.services.subscribe.score import get_score_subscribes
from app.services.subscribe.wrapper import handle_message, get_subs, handle_rm

__plugin_name__ = "订阅"
__plugin_short_description__ = "订阅 通知/成绩/考试 等，命令： subscribe"
__plugin_usage__ = r"""添加订阅：
    - 订阅
    - 添加订阅
    - 新建订阅
    - subscribe
    然后会提示输入序号，你也可以直接在后面加上序号，如：
        - 订阅 1
查看订阅：
    - 查看订阅
    - 订阅列表
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

cg = CommandGroup(
    "subscribe", permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
)


def get_subscribe_lst() -> str:
    msg = ""
    msg += get_rss_list().strip() + "\n"
    msg += get_score_subscribes().strip() + "\n"

    return msg


@cg.command(
    "subscribe", aliases=["subscribe", "订阅", "添加订阅", "新增订阅", "新建订阅"], only_to_me=False
)
async def subscribe(session: CommandSession):
    message = session.get(
        "message",
        prompt=f"你想订阅什么内容呢？（请输入序号，也可输入 `取消、不` 等语句取消）：\n{get_subscribe_lst()}",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )
    await handle_message(session.event, message)


@subscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


@cg.command("show", aliases=["查看订阅", "我的订阅", "订阅列表"], only_to_me=False)
async def _(session: CommandSession):
    subs = session.state.get("subs") or await get_subs(session.event)

    if not subs:
        session.finish("你还没有订阅任何内容哦")

    for k, v in subs.items():
        await session.send(format_subscription(k, v))
        await asyncio.sleep(0.05)
    session.finish(f"以上是所有的 {len(subs)} 个订阅")


@cg.command("rm", aliases=["取消订阅", "停止订阅", "关闭订阅", "删除订阅", "移除订阅"], only_to_me=False)
async def unsubscribe(session: CommandSession):
    subs = await get_subs(session.event)
    logger.info(f"subs: {subs}",)
    index: Optional[str] = session.state.get("index")
    logger.info(f"session.state: {session.state}",)
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
            prompt="你想取消哪一个订阅呢？（请发送序号，或者 `取消`）",
            arg_filters=[
                extractors.extract_text,
                controllers.handle_cancellation(session),
            ],
        )

    if index:
        await handle_rm(session.event, index)


@unsubscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["index"] = session.current_arg


def format_subscription(k, v) -> str:
    return f"序号：{k}\n" f"订阅名称：" f"{v}\n"
