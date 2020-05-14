import re
from typing import List

import nonebot as nb
from nonebot import context_id, scheduler as nbscheduler

from aiocqhttp import Event
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.base import JobLookupError
from apscheduler.job import Job


from ..aio import run_sync_func

scheduler = AsyncIOScheduler()


async def init_scheduler():
    _bot = nb.get_bot()
    jobstores = {"default": RedisJobStore(host="redis", port=6379, db=13)}  # 存储器
    if nbscheduler and nbscheduler.running:
        nbscheduler.shutdown(wait=False)

    if scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG, jobstores=jobstores)
        scheduler.start()


def make_job_id(plugin_name: str, event: Event = None, job_name: str = "") -> str:
    """
    Make a scheduler job id.
    :param plugin_name: the plugin that the user is calling
    :param context_id: context id
    :param job_name: name of the job, if not given, job id prefix is returned
    :return: job id, or job id prefix if job_name is not given
    """
    job_id = f"/{plugin_name}"
    if event:
        job_id += context_id(event)

    if job_name:
        if not re.fullmatch(r"[_a-zA-Z][_a-zA-Z0-9]*", job_name):
            raise ValueError(r'job name should match "[_a-zA-Z][_a-zA-Z0-9]*"')
        job_id += f"/{job_name}"
    return job_id


async def get_job(job_id: str) -> Job:
    """Get a scheduler job by id."""
    return await run_sync_func(scheduler.get_job, job_id)


async def get_jobs(job_id_prefix: str) -> List[Job]:
    """Get all scheduler jobs with given id prefix."""
    all_jobs = await run_sync_func(scheduler.get_jobs)
    return list(
        filter(
            lambda j: j.id.rsplit("/", maxsplit=1)[0] == job_id_prefix.rstrip("/"),
            all_jobs,
        )
    )


async def remove_job(job_id: str) -> bool:
    """Remove a scheduler job by id."""
    try:
        await run_sync_func(scheduler.remove_job, job_id)
        return True
    except JobLookupError:
        return False


async def add_job(func, **kwargs) -> Job:
    return await run_sync_func(scheduler.add_job, func, **kwargs)
