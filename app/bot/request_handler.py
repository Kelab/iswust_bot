from nonebot import on_request, RequestSession


# 好友请求处理器
@on_request("friend")
async def _(session: RequestSession):
    await session.approve()
    await session.send("你可以向我发送 <帮助> 查看我的使用指南。")
    await session.send("在输入框内输入 帮助 二字，点击发送按钮，然后按我的回复进行下一步的操作。")


@on_request("group.invite")
async def group(session: RequestSession):
    await session.approve()
    await session.send("你可以向我发送 <帮助> 查看我的使用指南。")
    await session.send("在输入框内输入 帮助 二字，点击发送按钮，然后按我的回复进行下一步的操作。")
