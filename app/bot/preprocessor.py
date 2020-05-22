import regex as re
from aiocqhttp import Event
from loguru import logger
from nonebot import Message, NoneBot, message_preprocessor
from nonebot.helpers import send

from app.libs.qqai_async.aaiasr import check_qqai_key, echo

record_re = re.compile(r"^\[CQ:record,file=([A-Z0-9]{32}\.silk)\]$")


@message_preprocessor
async def audio_preprocessor(bot: NoneBot, event: Event, *args):
    raw_message: str = event["raw_message"]
    logger.info(event)
    if raw_message.startswith("[CQ:record,"):
        if not check_qqai_key():
            return

        logger.info(f"raw_message: {raw_message}")
        await send(bot, event, "正在识别语音...")

        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(raw_message)
        if not match:
            return

        result, rec_text = await echo(match.group(1))
        logger.info(f"result: {result}, rec_text: {rec_text}")

        if result:
            event["message"] = Message(rec_text)
            event["raw_message"] = rec_text
            await send(bot, event, f"语音识别结果：{rec_text}")
        else:
            event["message"] = Message("")
            event["raw_message"] = ""
            await send(bot, event, f"语音识别失败，原因：{rec_text}")

        event["preprocessed"] = True
