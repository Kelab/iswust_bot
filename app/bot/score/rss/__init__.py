from apscheduler.triggers.interval import IntervalTrigger
from httpx import ConnectTimeout
from loguru import logger
from nonebot import CommandGroup, CommandSession
from nonebot.command.argfilter import controllers, validators

from app.config import Config
from app.libs.scheduler import scheduler
from app.models.subscribe import SubContent, SubUser

rss_cg = CommandGroup("rss", only_to_me=False)


@rss_cg.command("add", only_to_me=False)
async def add(session: CommandSession):
    url = session.get(
        "url",
        prompt="请输入你要订阅的地址：",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )
    if not session.state.get("silent"):
        await session.send(f"正在处理订阅链接：{url}")

    try:
        sub = await SubUser.get_sub(session.event, url)
        if sub:
            await session.send(f"{sub.sub_content.name} 已订阅~")
            return
        title = await SubUser.add_sub(session.event, url)
        if title:
            await session.send(f"{title} 订阅成功~")
            return
    except ConnectTimeout as e:
        logger.exception(e)
        await session.send("获取订阅源超时，请稍后重试。")
    except Exception as e:
        logger.exception(e)
        await session.send("订阅失败，请稍后重试。")


@add.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.rstrip()
    if session.is_first_run:
        if stripped_arg:
            session.state["url"] = stripped_arg
        return

    if not stripped_arg:
        session.pause("链接不能为空呢，请重新输入")

    session.state[session.current_key] = stripped_arg


@scheduler.scheduled_job(
    IntervalTrigger(seconds=Config.SUBSCIBE_INTERVAL, jitter=60), id="rss_update",
)
async def rss_update():
    await SubContent.check_update()
