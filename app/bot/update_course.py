from nonebot import CommandSession, on_command
from nonebot.command import call_command
import httpx
from app.services.course import CourseService
from loguru import logger


__plugin_name__ = "更新课表(命令：uc)"
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()


@on_command("uc", aliases=("更新课表",))
async def uc(session: CommandSession):
    sender_qq = session.ctx.get("user_id")
    await session.send(f"正在更新课表...")
    try:
        r: AsyncResponse = await CourseService.get_course(
            sender_qq, params={"update": "1"}, timeout=30,
        )
    except ReadTimeout:
        await session.send(f"课表正在更新中，请稍候直接查询。")

    if r:
        resp = await r.json()
        if resp["code"] == 200:
            logger.debug(f"更新课表结果：{str(resp)}")
            await call_command(
                session.bot, session.ctx, "cs", args={"course_schedule": resp}
            )
            await session.finish(f"更新成功")
            return
        await session.finish(
            f"更新出错，{resp['msg'].encode('gb18030').decode(encoding='utf-8')}"
        )
        return

    await session.finish("更新出错")
