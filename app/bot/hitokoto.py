from typing import Optional

from nonebot import CommandSession, on_command
import httpx

__plugin_name__ = "一言"
__plugin_usage__ = r"""给你回复一句话
""".strip()


@on_command("hitokoto", aliases=("一言",))
async def _(session: CommandSession):
    _hitokoto = await hitokoto()
    if _hitokoto:
        await session.send(f"送你一句话~")
        await session.finish(_hitokoto["hitokoto"].strip())
    await session.finish("那就祝你早安，午安，晚安吧")


async def hitokoto() -> Optional[dict]:
    # https://hitokoto.cn/api
    hitokoto_url = "https://international.v1.hitokoto.cn/"
    async with httpx.AsyncClient() as client:
        r: httpx.Response = await client.get(hitokoto_url)
        res = r.json()
    return res
