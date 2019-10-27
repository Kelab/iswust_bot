import regex as re

from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot import message_preprocessor
from nonebot import NoneBot, MessageSegment

from app.utils.asr_rec import echo

record_re = re.compile(r"^\[CQ:record,file=([A-Z0-9]{32}\.(silk|amr))\]$")


@message_preprocessor
async def audio_preprocessor(bot: NoneBot, ctx: dict):
    raw_message: str = ctx["raw_message"]

    if raw_message.startswith("[CQ:record,"):
        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(raw_message)
        if not match:
            return

        filename = match.group(1)
        result, rec_text = await echo(filename)
        if result:
            ctx["message"] = MessageSegment.text(rec_text)
            ctx["raw_message"] = rec_text
            await bot.send(ctx, f"语音识别结果：{rec_text}")
        else:
            ctx["message"] = MessageSegment.text("")
            ctx["raw_message"] = ""
            await bot.send(ctx, f"语音识别失败，原因：{rec_text}")
        ctx["preprocessed"] = True


@on_natural_language()
async def _(session: NLPSession):
    msg: str = session.ctx["raw_message"]

    if not ("课" in msg):
        await session.send(f"我不知道该说些什么啦~")
        return IntentCommand(90.0, "hitokoto")
