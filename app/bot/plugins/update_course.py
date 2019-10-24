from nonebot import CommandSession, on_command
from nonebot.command import call_command

from app.bot.constants.config import api_url
from utils.aio.requests import AsyncResponse
from services.course import CourseService
from log import IS_LOGGER

__plugin_name__ = "更新课表(命令：uc)"
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()


@on_command("uc", aliases=("更新课表", ))
async def uc(session: CommandSession):
    sender_qq = session.ctx.get("user_id")
    await session.send(f"正在更新课表...")
    r: AsyncResponse = await CourseService.get_course(
        sender_qq,
        params={"update": "1"},
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
