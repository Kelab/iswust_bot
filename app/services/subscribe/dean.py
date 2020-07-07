from typing import Dict, Tuple

from aiocqhttp import Event
from apscheduler.job import Job
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from app.bot.score.service import ScoreService
from app.config import Config
from app.libs.scheduler import add_job, get_jobs, make_job_id, remove_job
from app.models.score import PlanScore
from app.utils.score import save_score

from app.models.user import User

from . import BaseSub

PLUGIN_NAME = "sub_score_update"


class CheckUpdate:
    @staticmethod
    async def score(event: Event, **kwargs):
        logger.info(f"检查 {event.user_id} 是否有新成绩")
        user = await User.check(event.user_id)
        if not user:
            return
        score = await ScoreService._get_score(user)
        await PlanScore.check_update(event, score["plan"])
        await save_score(user, score)

    @staticmethod
    async def exam(event: Event, **kwargs):
        logger.info(f"检查 {event.user_id} 是否有新考试")
        user = await User.check(event.user_id)
        if not user:
            return


class DeanSub(BaseSub):
    PREFIX = "s"
    sub_info = {"有新成绩出来时提醒我": "score", "有新考试出来提醒我": "exam"}

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        return cls.dct()

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        jobs = await get_jobs(make_job_id(PLUGIN_NAME, event))
        for job in jobs:
            job: Job
            key = job.kwargs["key"]
            result[key] = cls.dct()[key]

        return result

    @classmethod
    async def del_sub(cls, event: Event, key: str) -> Tuple[bool, str]:
        name = cls.dct().get(key, "")
        if name:
            res = await remove_job(make_job_id(PLUGIN_NAME, event, key))
            if res:
                return True, f"删除 `{name}` 成功"
            else:
                return False, f"删除 `{name}` 失败，请稍后再试"
        else:
            return False, "输入有误"

    @classmethod
    async def add_sub(cls, event: Event, key: str) -> Tuple[bool, str]:
        name = cls.dct().get(key, "")
        cmd = cls.sub_info.get(name, "")
        func = getattr(CheckUpdate, cmd, None)
        if func:
            await add_job(
                func=func,
                trigger=IntervalTrigger(
                    seconds=Config.CACHE_SESSION_TIMEOUT + 120, jitter=10
                ),
                args=(event,),
                id=make_job_id(PLUGIN_NAME, event, key),
                misfire_grace_time=60,
                job_defaults={"max_instances": 10},
                replace_existing=True,
                kwargs={"key": key},
            )
            return True, f"添加 `{name}` 成功！"
        else:
            return False, "输入序号有误"
