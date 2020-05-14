from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot import CommandSession, on_command


@on_command("credit", aliases=("绩点", "我的绩点"))
async def _(session: CommandSession):
    session.finish("还不想实现")
    sender_qq = session.event.get("user_id")
