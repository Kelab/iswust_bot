from typing import Optional

from aiocqhttp import Event
from loguru import logger
from nonebot import get_bot
import pandas as pd

from app.config import Config
from app.libs.aio import run_sync_func
from app.libs.cache import cache
from app.libs.scheduler import add_job
from app.models.score import PlanScore
from app.models.user import User
from app.utils.bot import qq2event
from .parse import parse_score, ScoreDict
from .utils import (
    diff_score,
    send_score,
    tabulate,
    save_score,
    save_cet_score,
    send_cet_score,
)


class ScoreService:
    @classmethod
    async def check_update(cls, event: Event, plan: pd.DataFrame):
        old_score = await PlanScore.load_score(event)
        if old_score is None:
            return
        diffs = diff_score(plan, old_score)
        if not diffs.empty:
            bot = get_bot()
            await bot.send(event, f"有新的成绩：\n{tabulate(diffs)}")

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
    async def send_cet_score(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._send_cet_score, args=[user])
        _bot = get_bot()
        await _bot.send(qq2event(qq), "正在抓取成绩，抓取过后我会直接发给你！")
        return "WAIT"

    @classmethod
    async def _send_cet_score(cls, user: User):
        _bot = get_bot()
        try:
            res: ScoreDict = await cls._get_score(user)
            await save_cet_score(user, res)
            await send_cet_score(user, res)
        except Exception as e:
            logger.exception(e)
            await _bot.send(qq2event(user.qq), "查询成绩出错，请稍后再试")

    @classmethod
    async def _get_score(cls, user: User) -> ScoreDict:
        key = f"score/{user.qq}"
        res = await cache.get(key)
        if not res:
            sess = await User.get_session(user)
            res: ScoreDict = await run_sync_func(parse_score, sess)
            if res:
                await cache.set(key, res, ttl=Config.CACHE_SESSION_TIMEOUT)
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
