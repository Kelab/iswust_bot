from aiocqhttp import Event
from nonebot import get_bot

from app.models.chat_records import ChatRecords
from app.utils.bot import switch_session

PLUGIN_NAME = "save_chat_records"
__plugin_name__ = "再次执行上一句消息"
__plugin_short_description__ = "命令：re"
__plugin_usage__ = r"""
发送 re 让我重新执行你上一次发的消息
""".strip()

bot = get_bot()


@bot.on_message()
async def _(event: Event):
    if event.raw_message == "re":
        chat_record = await ChatRecords.get_last_msg(event)
        await switch_session(event, chat_record.msg)
    else:
        await ChatRecords.add_msg(event)
