import asyncio

from nonebot import on_natural_language, NLPSession, get_bot
from app.models.chat_records import ChatRecords

PLUGIN_NAME = "save_chat_records"

bot = get_bot()
lock = asyncio.Lock()


@on_natural_language(only_to_me=False, only_short_message=False)
async def _(session: NLPSession):
    async with lock:
        await ChatRecords.add_msg(session.event)
