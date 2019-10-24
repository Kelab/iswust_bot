import regex as re

from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot import message_preprocessor
from nonebot import NoneBot, Message

from app.utils.qqai_async.aaiasr import rec_silk

record_re = re.compile(r"\[CQ:record,file=([A-Z0-9]{32}\.silk)\]")


@message_preprocessor
async def audio_preprocessor(bot: NoneBot, ctx: dict):
    msg: str = ctx["raw_message"]

    if msg.startswith("[CQ:record,"):
        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(msg)
        if not match:
            return

        filename = match.group(1)
        result, text = await rec_silk(filename)
        if result:
            ctx["message"] = Message(text)
            ctx["raw_message"] = text
            await bot.send(ctx, f"语音识别结果：{text}")
        else:
            ctx["message"] = Message([""])
            ctx["raw_message"] = ""
            await bot.send(ctx, f"语音识别失败，原因：{text}")
        ctx["preprocessed"] = True


@on_natural_language()
async def _(session: NLPSession):
    msg: str = session.ctx["raw_message"]

    if not ("课" in msg):
        await session.send(f"我不知道该说些什么啦~")
        return IntentCommand(90.0, "hitokoto")
