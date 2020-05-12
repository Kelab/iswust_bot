from nonebot import CommandSession, on_command

from app.models.user import User

__plugin_name__ = "取消绑定教务处(命令：unbind)"
__plugin_usage__ = r"""取消绑定教务处
使用方法：向我发送以下指令。
    unbind
    取消绑定
    解绑
    """


@on_command("unbind", aliases=("解绑", "取消绑定", "取消绑定教务处"))
async def unbind(session: CommandSession):
    r = await User.unbind(session.event.user_id)
    if r:
        session.finish("取消绑定成功")
    session.finish("取消绑定失败")
