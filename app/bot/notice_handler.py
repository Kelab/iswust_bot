from loguru import logger

from nonebot import on_notice, NoticeSession


@on_notice
async def _(session: NoticeSession):
    logger.info(f"有新的通知事件：{session.event}")


@on_notice("group_increase")
async def _(session: NoticeSession):
    await session.send("欢迎新朋友～")
