from typing import Optional

from nonebot import get_bot

from app.libs.aio import run_sync_func
from app.libs.scheduler import add_job
from app.models.user import User
from app.utils.bot import qq2event
from app.utils.parse.credit_progress import get_credit_progress

_bot = get_bot()


class CreditService:
    @classmethod
    async def get_progress(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._get_progress, args=[user])
        await _bot.send(qq2event(qq), "正在抓取绩点，抓取过后我会直接发给你！")
        return "WAIT"

    @classmethod
    async def _get_progress(cls, user: User):
        sess = await User.get_session(user)
        res = await run_sync_func(get_credit_progress, sess)
        if res:
            await _bot.send(qq2event(user.qq), _format(res))
            return
        await _bot.send(qq2event(user.qq), "查询绩点出错，请稍后再试")


def _format(credits: dict):
    msg = ""
    for name, credit in credits.items():
        msg = msg + f"{name}: {credit}\n"
    return msg.strip()
