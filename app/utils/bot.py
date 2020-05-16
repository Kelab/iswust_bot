from aiocqhttp import Event
from loguru import logger
from nonebot import get_bot
import asyncio


def ctx_id2event(ctx_id: str):
    if ctx_id.startswith("/group/"):
        return Event(group_id=ctx_id.replace("/group/", "").split("/")[0])
    if ctx_id.startswith("/discuss/"):
        return Event(discuss_id=ctx_id.replace("/discuss/", "").split("/")[0])
    if ctx_id.startswith("/user/"):
        return Event(user_id=ctx_id.replace("/user/", "").split("/")[0])
    return Event()


async def send_msgs(event: Event, msgs):
    if not msgs:
        return
    bot = get_bot()
    for msg in msgs:
        logger.info(f"给 {event} 发送: {msg}")
        await bot.send(event, msg)


def qq2event(qq: int):
    return Event(user_id=qq)
