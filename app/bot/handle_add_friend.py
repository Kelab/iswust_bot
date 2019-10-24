import os
from nonebot import on_request, RequestSession


# 好友请求处理器
@on_request("friend")
async def _(session: RequestSession):
    an_hao = os.environ.get("AN_HAO") or "请输入暗号"
    if session.ctx["comment"] == an_hao:
        await session.approve()
        await session.send("你可以向我发送 <帮助> 查看我的使用指南。")
        await session.send("在输入框内输入 帮助 二字，点击发送按钮，然后按我的回复进行下一步的操作。")

    else:
        await session.reject()
