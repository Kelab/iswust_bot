from nonebot import on_command, CommandSession
from iswust.constants.urls import API
from iswust.constants.tools import xor_encrypt

import requests
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
    r = requests.get(API.api_url + 'api/v1/unbind',
                     data={"verifycode": xor_encrypt(sender_qq)})
    print(r)
    if r and r.status_code == 200 and r.json():
        session.finish('取消绑定成功')
    else:
        session.finish('您未绑定教务处账号')
