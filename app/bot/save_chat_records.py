import asyncio

from nonebot import on_natural_language, NLPSession, get_bot
from app.models.chat_records import ChatRecords

PLUGIN_NAME = "save_chat_records"

bot = get_bot()
lock = asyncio.Lock()


@on_natural_language(only_to_me=False, only_short_message=False)
async def _(session: NLPSession):
    # we don't want to block the processing of message,
    # so just make sure it will append in the future
    asyncio.ensure_future(append_message(session.event))


async def append_message(event) -> None:
    async with lock:
        await ChatRecords.add_msg(event)
