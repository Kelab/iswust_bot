from typing import Dict, Any, Union, List, Tuple

import nonebot as nb
from nonebot.command import call_command

from aiocqhttp import Event
from apscheduler.job import Job
from apscheduler.jobstores.base import ConflictingIdError

from . import scheduler
from .exception import JobIdConflictError
from ..aio import run_sync_func


class ScheduledCommand:
    """
    Represent a command that will be run when a scheduler job
    being executing.
    """

    __slots__ = ("name", "current_arg")

    def __init__(self, name: Union[str, Tuple[str]], current_arg: str = ""):
        self.name = name
        self.current_arg = current_arg

    def __repr__(self):
        return (
            f"<ScheduledCommand ("
            f"name={repr(self.name)}, "
            f"current_arg={repr(self.current_arg)})>"
        )

    def __str__(self):
        return f"{self.name}" f'{" " + self.current_arg if self.current_arg else ""}'


async def add_scheduled_commands(
    commands: Union[ScheduledCommand, List[ScheduledCommand]],
    *,
    job_id: str,
    event: Event,
    trigger: str,
    replace_existing: bool = False,
    misfire_grace_time: int = 360,
    apscheduler_kwargs: Dict[str, Any] = None,
    **trigger_args,
) -> Job:
    """
    Add commands to scheduler for scheduled execution.
    :param commands: commands to add, can be a single ScheduledCommand
    :param job_id: job id, using of make_job_id() is recommended
    :param event: context dict
    :param trigger: same as APScheduler
    :param replace_existing: same as APScheduler
    :param misfire_grace_time: same as APScheduler
    :param apscheduler_kwargs: other APScheduler keyword args
    :param trigger_args: same as APScheduler
    """
    commands = [commands] if isinstance(commands, ScheduledCommand) else commands

    try:
        return await run_sync_func(
            scheduler.add_job,
            _scheduled_commands_callback,
            id=job_id,
            trigger=trigger,
            **trigger_args,
            kwargs={"event": event, "commands": commands},
            replace_existing=replace_existing,
            misfire_grace_time=misfire_grace_time,
            **(apscheduler_kwargs or {}),
        )
    except ConflictingIdError:
        raise JobIdConflictError(job_id)


async def _scheduled_commands_callback(
    event: Event, commands: List[ScheduledCommand]
) -> None:
    # get the current bot, we may not in the original running environment now
    bot = nb.get_bot()
    for cmd in commands:
        await call_command(
            bot,
            event,
            cmd.name,
            current_arg=cmd.current_arg,
            check_perm=True,
            disable_interaction=True,
        )


def get_scheduled_commands_from_job(job: Job) -> List[ScheduledCommand]:
    """Get list of ScheduledCommand from a job."""
    return job.kwargs["commands"]
