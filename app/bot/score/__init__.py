from nonebot import on_command, CommandSession

__plugin_name__ = "查询成绩"
__plugin_usage__ = r"""输入 查询成绩/成绩
    使用方法：
    成绩"""


@on_command("score", aliases=("查询成绩", "成绩"))
async def score(session: CommandSession):
    session.finish("暂未实现")


@score.args_parser
async def _(session: CommandSession):
    pass
