from nonebot import (NLPSession, on_natural_language)

from typing import Optional

from utils.aio import requests
from requests import Response


@on_natural_language()
async def _(session: NLPSession):
    await session.send(f"我不知道该说些什么啦~")
    _hitokoto = await hitokoto()
    if _hitokoto:
        resp = f"{_hitokoto['from']}:\n{_hitokoto['hitokoto']}"
        await session.finish(resp)
        return
    await session.finish("那就祝你早安，午安，晚安吧")


async def hitokoto() -> Optional[dict]:
    # https://hitokoto.cn/api
    hitokoto_url = "https://international.v1.hitokoto.cn/"

    r: Response = await requests.get(hitokoto_url)
    res = await r.json()

    return res
