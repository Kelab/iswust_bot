import asyncio
from typing import Optional

from base64 import b64encode

from aiocqhttp import Event
from nonebot import CommandGroup, CommandSession
from nonebot import permission as perm
from nonebot.command import call_command
from nonebot.command.argfilter import controllers, extractors, validators

from app.services.subscribe.wrapper import SubWrapper, judge_sub
from app.utils.api import to_token
from urllib.parse import urlencode
from app.config import Config

__plugin_name__ = "订阅"
__plugin_short_description__ = "订阅 通知/成绩/考试 等，命令： subscribe"
__plugin_usage__ = r"""
帮助链接：https://bot.artin.li/guide/subscribe.html

添加订阅：
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


def get_subscribe_str() -> str:
    msg = ""
    dct = SubWrapper.get_subs()
    for k, v in dct.items():
        msg = msg + f"{k}. {v}\n"

    return msg


@cg.command(
    "subscribe", aliases=["subscribe", "订阅", "添加订阅", "新增订阅", "新建订阅"], only_to_me=False
)
async def subscribe(session: CommandSession):
    message = session.get(
        "message",
        prompt=f"你想订阅什么内容呢？（请输入序号，也可输入 `取消、不` 等语句取消）：\n{get_subscribe_str()}",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.strip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )
    SubC = judge_sub(message)
    if not SubC:
        session.finish("输入序号有误！")

    _, msg = await SubC.add_sub(session.event, message)
    session.finish(msg)


@subscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


def get_user_center(event: Event):
    sender = event.get("sender", {})
    sender_qq: Optional[str] = sender.get("user_id")

    if sender_qq:
        token = to_token(sender_qq)
        # web 登录界面地址
        query: str = urlencode({"qq": sender_qq, "token": token})
        encoded_query = b64encode(query.encode("utf8")).decode("utf8")
        return f"{Config.WEB_URL}/user/?{encoded_query}"


@cg.command("show", aliases=["查看订阅", "我的订阅", "订阅列表"], only_to_me=False)
async def _(session: CommandSession):
    subs = session.state.get("subs") or await SubWrapper.get_user_sub(session.event)

    if not subs:
        session.finish("你还没有订阅任何内容哦")

    for k, v in subs.items():
        await session.send(format_subscription(k, v))
        await asyncio.sleep(0.05)
    await session.send(f"以上是所有的 {len(subs)} 个订阅")
    session.finish(f"订阅管理：{get_user_center(session.event)}")


@cg.command("rm", aliases=["取消订阅", "停止订阅", "关闭订阅", "删除订阅", "移除订阅"], only_to_me=False)
async def unsubscribe(session: CommandSession):
    subs = await SubWrapper.get_user_sub(session.event)
    key: Optional[str] = session.state.get("key")
    if key is None:
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

        key = session.get(
            "key",
            prompt="你想取消哪一个订阅呢？（请发送序号，或者 `取消`）",
            arg_filters=[
                extractors.extract_text,
                controllers.handle_cancellation(session),
            ],
        )

    if key:
        SubC = judge_sub(key)
        if not SubC:
            session.finish("输入序号有误！")

        _, msg = await SubC.del_sub(session.event, key)
        session.finish(msg)


@unsubscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["key"] = session.current_arg


def format_subscription(k, v) -> str:
    return f"序号：{k}\n" f"订阅名称：" f"{v}\n"
