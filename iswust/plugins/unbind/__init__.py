from nonebot import on_command, CommandSession
from iswust.models import User
__plugin_name__ = '取消绑定教务处'
__plugin_usage__ = r"""取消绑定教务处
使用方法：
    /unbind
    /取消绑定
    /取消绑定
    """


@on_command('unbind', aliases=('取消绑定', '取消绑定教务处'))
async def unbind(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    user_query = await User.query.where(User.qq == sender_qq).gino.first()
    if user_query:
        await user_query.delete()
        session.finish('取消绑定成功')
    else:
        session.finish('您未绑定教务处账号')
