from nonebot import CommandSession, on_command
from app.services.credit import CreditService


@on_command("credit", aliases=("绩点", "我的绩点"))
async def _(session: CommandSession):
    sender_qq = session.event.get("user_id")
    try:
        resp = await CreditService.get_progress(sender_qq)

        if not resp:
            await session.send("查询出错")
            return

        if resp == "WAIT":
            await session.send("正在抓取绩点，抓取过后我会直接发给你！")
            return
        elif resp == "NOT_BIND":
            return

    except Exception:
        await session.send("查询出错")
