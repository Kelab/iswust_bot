from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot import CommandSession, on_command


@on_command("饭卡余额", aliases=("余额", "一卡通余额"))
async def _(session: CommandSession):
    session.finish("待实现")


@on_command("饭卡消费", aliases=("消费", "消费记录"))
async def _(session: CommandSession):
    session.finish("待实现")


@on_natural_language(["饭卡", "一卡通", "ecard"])
async def _(session: NLPSession):
    msg: str = session.ctx["raw_message"]

    if "消费" in msg:
        return IntentCommand(90.0, "饭卡消费")
    return IntentCommand(90.0, "饭卡余额")
