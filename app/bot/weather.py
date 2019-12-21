from typing import Optional

from nonebot import CommandSession, on_command
from requests import Response
from app.services.weather import Weather
__plugin_name__ = "天气"
__plugin_usage__ = r"""使用方法：
天气 城市
""".strip()


@on_command("weather", aliases=("天气", ))
async def _(session: CommandSession):
    arg = session.current_arg_text
    if not arg:
        arg = "绵阳"
    msg = await Weather.get(arg)
    await session.finish(msg)
