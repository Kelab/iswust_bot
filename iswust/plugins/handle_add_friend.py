from nonebot import on_request, RequestSession


# 好友请求处理器
@on_request('friend')
async def _(session: RequestSession):
    if session.ctx['comment'] == '123123':
        await session.approve()
        return
    await session.reject('暗号错误')
