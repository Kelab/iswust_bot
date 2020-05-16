from loguru import logger
from nonebot import CommandSession, on_command

from .service import CreditService


@on_command("credit", aliases=("绩点", "我的绩点"))
async def _(session: CommandSession):
    sender_qq = session.event.get("user_id")
    try:
        await CreditService.get_progress(sender_qq)
    except Exception as e:
        logger.exception(e)
        await session.send("查询出错")
