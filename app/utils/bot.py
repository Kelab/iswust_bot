import asyncio

from aiocqhttp import Event
from nonebot import get_bot
from nonebot.command import kill_current_session
from nonebot.message import Message, handle_message


def ctx_id2event(ctx_id: str):
    if ctx_id.startswith("/group/"):
        return Event(group_id=ctx_id.replace("/group/", "").split("/")[0])
    if ctx_id.startswith("/discuss/"):
        return Event(discuss_id=ctx_id.replace("/discuss/", "").split("/")[0])
    if ctx_id.startswith("/user/"):
        return Event(user_id=ctx_id.replace("/user/", "").split("/")[0])
    return Event()


async def send_msgs(event: Event, msgs):
    bot = get_bot()
    if not msgs:
        return
    for msg in msgs:
        await bot.send(event, msg)


def qq2event(qq: int):
    return Event(user_id=qq)


def replace_event_msg(event: Event, msg: str):
    new_event = Event.from_payload(event)
    new_event["message"] = Message(msg)
    new_event["raw_message"] = msg
    return new_event


async def switch_session(event, msg):
    bot = get_bot()
    kill_current_session(event)
    new_event = replace_event_msg(event, msg)
    await bot.send(new_event, "re: " + msg)
    event["to_me"] = True
    asyncio.ensure_future(handle_message(bot, new_event))
