from log import IS_LOGGER
from nonebot import on_notice, NoticeSession


@on_notice
async def _(session: NoticeSession):
    IS_LOGGER.info('有新的通知事件：%s', session.ctx)


@on_notice('group_increase')
async def _(session: NoticeSession):
    await session.send('欢迎新朋友～')
