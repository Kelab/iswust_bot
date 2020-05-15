from typing import Optional

from nonebot import get_bot

from app.libs.aio import run_sync_func
from app.libs.scheduler import add_job
from app.models.user import User
from app.utils.bot_common import qq2event
from app.utils.parse.ecard import get_ecard_balance


class ECardService:
    @classmethod
    async def get_balance(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._get_balance, args=[user])
        return "WAIT"

    @classmethod
    async def _get_balance(cls, user: User):
        sess = await User.get_session(user)
        res = await run_sync_func(get_ecard_balance, sess, user.student_id)
        _bot = get_bot()
        if res:
            await _bot.send(qq2event(user.qq), str(res))
            return
        await _bot.send(qq2event(user.qq), "查询余额出错，请稍后再试")
