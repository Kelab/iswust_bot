from nonebot import on_command, CommandSession
from .auth import login_jwc
from requests import ConnectionError
from iswust.models import User
import ujson
__plugin_name__ = '绑定教务处'
__plugin_usage__ = r"""输入账号密码绑定教务处
使用方法：
    /绑定 [学号] [密码]
    /绑定教务处 [学号] [密码]
    /bind [学号] [密码]"""


@on_command('bind', aliases=('绑定', '绑定教务处'))
async def bind(session: CommandSession):
    username_password = session.get('username_passwd_li',
                                    prompt='请输入学号密码，用空格隔开（无需加 /bind）')
    try:
        result, response = await login_jwc(username_password[0],
                                           username_password[1], session.ctx)
        if result is True:
            try:
                data = response.json()
                result = data['body']['result']
                print(result)

                result = ujson.loads(result)
                class_ = result.get('class')
                name = result.get('name')

                await session.send(f'{class_}{name}你好，您已绑定成功')
            except Exception:
                await session.send(f'您已绑定成功')
            finally:
                await session.send('输入 /帮助 获取帮助')
        else:
            await session.send(result)

    except ConnectionError:
        await session.send("教务处未响应我们的请求，请检查教务处是否能访问。")


@bind.args_parser
async def _(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    user_query = await User.query.where(User.qq == sender_qq).gino.first()
    if user_query:
        session.finish('您已绑定，输入取消绑定可取消绑定')

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
