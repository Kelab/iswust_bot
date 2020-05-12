from nonebot import CommandSession, on_command
from nonebot.command import call_command
from loguru import logger
from app.models.course import CourseStudent

__plugin_name__ = "更新课表(命令：uc)"
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()


@on_command("uc", aliases=("更新课表",))
async def uc(session: CommandSession):
    sender_qq = session.event.get("user_id")
    await session.send(f"正在更新课表...")
    try:
        resp = await CourseStudent.update_course(sender_qq)
    except Exception:
        await session.send(f"课表正在更新中，请稍候查询。")
        return

    if resp:
        logger.debug(f"更新课表结果：{str(resp)}")
        await call_command(
            session.bot, session.event, "cs", args={"course_schedule": resp}
        )
        await session.finish(f"更新成功")
        return

    session.finish("更新出错")
