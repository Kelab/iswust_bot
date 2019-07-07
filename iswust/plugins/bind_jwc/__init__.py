from nonebot import on_command, CommandSession
from .auth import login_jwc
from ...constants.urls import API

__plugin_name__ = '绑定教务处'
__plugin_usage__ = r"""输入账号密码绑定教务处
    使用方法：
    /绑定 [学号] [密码]"""


@on_command('bind', aliases=('绑定'))
async def bind(session: CommandSession):
    username_password = session.get('username_passwd_li',
                                    prompt='请输入学号密码，用空格隔开（无需加 /bind）')
    result = await login_jwc(username_password[0], username_password[1],
                             session.ctx)
    if result is True:
        await session.send('绑定成功')
        await session.send('输入 /帮助 获取帮助')

    else:
        await session.send(result)


@bind.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    print(session.current_arg_text)
    if session.is_first_run:
        if stripped_arg:
            try:
                username_password = stripped_arg.split()
                session.state['username_passwd_li'] = username_password
            except ValueError:
                session.pause('学号密码输入错误，请重新输入（无需加 /bind）')
        return

    if not stripped_arg:
        session.pause('未输入学号密码，请输入')
    try:
        username_password = stripped_arg.split()
        session.state['username_passwd_li'] = username_password
    except ValueError:
        session.pause('学号密码输入错误，请重新输入（无需加 /bind）')
