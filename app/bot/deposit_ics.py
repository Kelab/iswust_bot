from nonebot import CommandSession, on_command
from app.services.course import CourseService
from loguru import logger

__plugin_name__ = "托管课表生成的日历(命令：托管日历)"
__plugin_usage__ = r"""输入 托管日历
然后我会给你一个日历的在线地址，日历每天更新
""".strip()


@on_command("deposit_ics", aliases=("托管日历",))
async def uc(session: CommandSession):
    session.finish("还不想实现")

    sender_qq = session.event.get("user_id")
    logger.info(f"{sender_qq} 请求托管日历。")
    r = await CourseService.deposit_ics(sender_qq)
    if r:
        resp = r.json()
        if resp["code"] == 200:
            await session.send(f"托管日历成功！")
            await session.send(f"日历地址我稍后会发送给你。")
            return
        session.finish(
            f"托管日历出错，{resp['msg'].encode('gb18030').decode(encoding='utf-8')}"
        )
        return

    session.finish("托管日历出错")
