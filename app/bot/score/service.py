from typing import Optional

from loguru import logger
from nonebot import get_bot

from app.config import Config
from app.libs.aio import run_sync_func
from app.libs.cache import cache
from app.libs.scheduler import add_job
from app.models.score import save_score
from app.models.user import User
from app.utils.bot import qq2event
from app.utils.parse.score import ScoreDict, parse_score

from .utils import send_score


class ScoreService:
    @classmethod
    async def send_score(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._send_score, args=[user])
        _bot = get_bot()
        await _bot.send(qq2event(qq), "正在抓取成绩，抓取过后我会直接发给你！")
        return "WAIT"

    @classmethod
    async def _get_score(cls, user: User) -> ScoreDict:
        key = f"score/{user.qq}"
        res = await cache.get(key)
        if not res:
            sess = await User.get_session(user)
            res: ScoreDict = await run_sync_func(parse_score, sess)
            if res:
                await cache.set(key, res, ttl=Config.CACHE_SCORE_INTERVAL)
            else:
                raise ValueError("查询成绩出错")
        return res

    @classmethod
    async def _send_score(cls, user: User):
        _bot = get_bot()
        try:
            res: ScoreDict = await cls._get_score(user)
            await save_score(user, res)
            await send_score(user, res)
        except Exception as e:
            logger.exception(e)
            await _bot.send(qq2event(user.qq), "查询成绩出错，请稍后再试")
