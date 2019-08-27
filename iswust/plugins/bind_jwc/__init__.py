from nonebot import on_command, CommandSession
from utils.tools import xor_encrypt, tcn
from iswust.constants.config import web_url
from typing import Optional, Any

__plugin_name__ = '绑定教务处'
__plugin_usage__ = r"""对我发以下关键词开始绑定：
绑定、绑定教务处、bind"""


@on_command('bind', aliases=('绑定', '绑定教务处'))
async def bind(session: CommandSession):
    await session.send(f'开始请求绑定~ 请等待')

    sender: dict[str, Any] = session.ctx.get('sender', {})
    sender_qq: Optional[str] = sender.get('user_id')

    nickname: Optional[str] = sender.get('nickname')

    if sender_qq:
        verify_code = xor_encrypt(int(sender_qq))

        # web 登录界面地址
        url_ = f'{web_url}?qq={sender_qq}&nickname={nickname}&verifycode={verify_code}'
        shorten_url_ = tcn(url_)
        if shorten_url_:
            await session.send(f'请点击链接绑定：{shorten_url_}')
        else:
            await session.send(f'请点击链接绑定：{url_}')
