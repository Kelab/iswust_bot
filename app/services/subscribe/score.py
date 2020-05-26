from aiocqhttp import Event
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from nonebot.command import _FinishException

from app.bot.score.service import ScoreService
from app.config import Config
from app.libs.scheduler import add_job, get_job, make_job_id, remove_job
from app.models.score import CETScore, PhysicalOrCommonScore, PlanScore, save_score
from app.models.user import User
from typing import Dict
from . import BaseSub

PLUGIN_NAME = "sub_score_update"


async def check_update(event: Event):
    logger.info(f"检查 {event.user_id} 是否有新成绩")
    user = await User.check(event.user_id)
    if not user:
        return
    score = await ScoreService._get_score(user)
    await PlanScore.check_update(event, score["plan"])

    await save_score(user, score)


class ScoreSub(BaseSub):
    PREFIX = "s"
    NAME = "有新成绩出来时提醒我"
    dct = {PREFIX: NAME}

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        return cls.dct

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        job = await get_job(make_job_id(PLUGIN_NAME, event))
        if job:
            result[cls.PREFIX] = cls.NAME
        return result

    @classmethod
    async def del_sub(cls, event: Event, key: str):
        if key.startswith(cls.PREFIX):
            res = await remove_job(make_job_id(PLUGIN_NAME, event))
            if res:
                await cls.bot.send(event, f"删除 `{cls.NAME}` 成功")
            else:
                await cls.bot.send(event, "删除失败，请稍后再试")

            raise _FinishException

    @classmethod
    async def add_sub(cls, event: Event, key: str):
        if key.startswith(cls.PREFIX):
            try:
                await add_job(
                    func=check_update,
                    trigger=IntervalTrigger(
                        seconds=Config.CACHE_SCORE_INTERVAL + 120, jitter=10
                    ),
                    args=(event,),
                    id=make_job_id(PLUGIN_NAME, event),
                    misfire_grace_time=60,
                    job_defaults={"max_instances": 10},
                    replace_existing=True,
                )
                await cls.bot.send(event, "添加成功！")
            except Exception as e:
                await cls.bot.send(event, "输入有误")
                logger.exception(e)
            raise _FinishException
