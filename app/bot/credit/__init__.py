from loguru import logger
from nonebot import CommandSession, on_command

from .service import CreditService

__plugin_name__ = "绩点"
__plugin_short_description__ = "命令：credit"
__plugin_usage__ = r"""
帮助链接：https://bot.artin.li/guide/credit.html

查看我的绩点：
命令：
    - credit
    - 绩点
    - 我的绩点
""".strip()


@on_command("credit", aliases=("绩点", "我的绩点"))
async def _(session: CommandSession):
    sender_qq = session.event["user_id"]
    try:
        await CreditService.get_progress(sender_qq)
    except Exception as e:
        logger.exception(e)
        await session.send("查询出错")
