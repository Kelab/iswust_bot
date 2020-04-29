import os
from loguru import logger
import regex as re
from nonebot import (
    message_preprocessor,
    MessageSegment,
    NoneBot,
)
from nonebot.helpers import send
from aiocqhttp import Event

from app.libs.qqai_async.aaiasr import echo


record_re = re.compile(r"^\[CQ:record,file=([A-Z0-9]{32}\.silk)\]$")


@message_preprocessor
async def audio_preprocessor(bot: NoneBot, event: Event, *args):
    raw_message: str = event["raw_message"]
    logger.info(event)
    if raw_message.startswith("[CQ:record,"):
        appid = os.environ.get("QQAI_APPID")
        appkey = os.environ.get("QQAI_APPKEY")

        if not appid or not appkey:
            logger.error("未设置 QQAI_APPID 和 QQAI_APPKEY！")
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
            event["message"] = MessageSegment.text(rec_text)
            event["raw_message"] = rec_text
            await send(bot, event, f"语音识别结果：{rec_text}")
        else:
            event["message"] = MessageSegment.text("")
            event["raw_message"] = ""
            await send(bot, event, f"语音识别失败，原因：{rec_text}")

        event["preprocessed"] = True
