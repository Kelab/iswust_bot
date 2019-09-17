from nonebot import on_command, CommandSession
from utils.tools import bot_hash
from app.bot.constants.config import api_url
from typing import Optional, Any

from utils.aio import requests
from requests import Response

__plugin_name__ = '取消绑定教务处'
__plugin_usage__ = r"""取消绑定教务处
使用方法：向我发送以下指令。
    /unbind
    /取消绑定
    /取消绑定
    """


@on_command('unbind', aliases=('解绑', '取消绑定', '取消绑定教务处'))
async def unbind(session: CommandSession):
    sender: dict[str, Any] = session.ctx.get('sender', {})
    sender_qq: Optional[str] = sender.get('user_id')
    if sender_qq:
        r: Response = await requests.get(api_url + 'api/v1/user/unbind',
                                         params={
                                             "qq": sender_qq,
                                             "token": bot_hash(sender_qq)
                                         })

        if r:
            resp = await r.json()
            session.finish(resp['msg'])
