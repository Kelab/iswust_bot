import os
from nonebot import on_request, RequestSession


# 好友请求处理器
@on_request("friend")
async def _(session: RequestSession):
    an_hao = os.environ.get("AN_HAO") or "请输入暗号"
    if session.ctx["comment"] == an_hao:
        await session.approve()
    else:
        await session.reject()
