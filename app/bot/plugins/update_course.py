from nonebot import CommandSession, on_command
from nonebot.command import call_command
from requests import Response

from app.bot.constants.config import api_url
from utils.aio import requests
from utils.tools import bot_hash
from log import IS_LOGGER

__plugin_name__ = "更新课表(命令：uc)"
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()


@on_command("uc", aliases=("更新课表", ))
async def uc(session: CommandSession):
    sender_qq = session.ctx.get("user_id")
    await session.send(f"正在更新课表...")
    r: Response = await requests.get(
        api_url + "api/v1/course/getCourse",
        params={
            "qq": sender_qq,
            "token": bot_hash(sender_qq),
            "update": "1"
        },
        timeout=10,
    )

    if r:
        resp = await r.json()
        if resp["code"] == 200:
            IS_LOGGER.debug(f"更新课表结果：{str(resp)}")
            await call_command(session.bot,
                               session.ctx,
                               "cs",
                               args={"course_schedule": resp})
            await session.finish(f"更新成功")
            return
        await session.finish(
            f"更新出错，{resp['msg'].encode('gb18030').decode(encoding='utf-8')}")
        return

    await session.finish("更新出错")
