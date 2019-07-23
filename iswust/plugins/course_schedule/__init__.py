from nonebot import on_command, CommandSession
from iswust.models import User
__plugin_name__ = '查询课表'
__plugin_usage__ = r"""输入 查询课表/课表"""


@on_command('course_schedule', aliases=('查询课表', '课表'))
async def grade(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    user_query = await User.query.where(User.qq == sender_qq).gino.first()

    await session.send('待实现')


@grade.args_parser
async def _(session: CommandSession):
    pass
