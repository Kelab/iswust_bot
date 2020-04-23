import aiocqhttp
import regex as re
from nonebot import (
    get_bot,
    message_preprocessor,
    MessageSegment,
    NoneBot,
)

from app.libs.qqai_async.aaiasr import echo

_bot = get_bot()

record_re = re.compile(r"^\[CQ:record,file=([A-Z0-9]{32}\.(silk|amr))\]$")


@message_preprocessor
async def audio_preprocessor(bot: NoneBot, ctx: dict):
    raw_message: str = ctx["raw_message"]

    if raw_message.startswith("[CQ:record,"):
        await bot.send(ctx, f"正在识别语音：{raw_message}")

        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(raw_message)
        if not match:
            return

        result, rec_text = await echo(match.group(1))

        if result:
            ctx["message"] = MessageSegment.text(rec_text)
            ctx["raw_message"] = rec_text
            await bot.send(ctx, f"语音识别结果：{rec_text}")
        else:
            ctx["message"] = MessageSegment.text("")
            ctx["raw_message"] = ""
            await bot.send(ctx, f"语音识别失败，原因：{rec_text}")
        ctx["preprocessed"] = True
