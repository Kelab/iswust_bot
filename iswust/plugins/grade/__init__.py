from nonebot import on_command, CommandSession

__plugin_name__ = '查询成绩'
__plugin_usage__ = r"""输入 查询成绩/成绩
    使用方法：
    成绩"""


@on_command('grade', aliases=('查询成绩', '成绩'))
async def grade(session: CommandSession):
    await session.send('待实现')


@grade.args_parser
async def _(session: CommandSession):
    pass
