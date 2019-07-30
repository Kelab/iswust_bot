from nonebot import on_command, CommandSession
from iswust.constants.tools import xor_encrypt
from iswust.constants.config import api_url

import requests
__plugin_name__ = '取消绑定教务处'
__plugin_usage__ = r"""取消绑定教务处
使用方法：向我发送以下指令。
    /unbind
    /取消绑定
    /取消绑定
    """


@on_command('unbind', aliases=('解绑', '取消绑定', '取消绑定教务处'))
async def unbind(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    r = requests.get(api_url + 'api/v1/user/unbind',
                     params={"verifycode": xor_encrypt(sender_qq)})
    print(r.json())
    if r and r.json():
        session.finish(r.json()['msg'])
