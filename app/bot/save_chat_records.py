from aiocqhttp import Event
from nonebot import get_bot

from app.models.chat_records import ChatRecords

PLUGIN_NAME = "save_chat_records"


bot = get_bot()


@bot.on_message()
async def _(event: Event):
    await ChatRecords.add_msg(event)
