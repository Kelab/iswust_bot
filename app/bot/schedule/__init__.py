import asyncio
import re
from typing import List

from apscheduler.job import Job
from nonebot import CommandGroup, CommandSession
from nonebot import permission as perm
from nonebot.argparse import ArgumentParser
from nonebot.command import CommandManager

from app.libs.scheduler import get_job, get_jobs, make_job_id, remove_job
from app.libs.scheduler.command import (
    ScheduledCommand,
    add_scheduled_commands,
    get_scheduled_commands_from_job,
)
from app.libs.scheduler.exception import JobIdConflictError

from . import usage

PLUGIN_NAME = "schedule"

cg = CommandGroup(
    PLUGIN_NAME, permission=perm.PRIVATE | perm.GROUP_ADMIN, shell_like=True
)


@cg.command("add", aliases=("schedule",))
async def sched_add(session: CommandSession):
    parser = ArgumentParser(session=session, usage=usage.ADD)
    parser.add_argument("-S", "--second")
    parser.add_argument("-M", "--minute")
    parser.add_argument("-H", "--hour")
    parser.add_argument("-d", "--day")
    parser.add_argument("-m", "--month")
    parser.add_argument("-w", "--day-of-week")
    parser.add_argument("-f", "--force", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("--name", required=True)
    parser.add_argument("commands", nargs="+")
    args = parser.parse_args(session.argv)

    if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*", args.name):
        await session.send("计划任务名必须仅包含字母、数字、下划线，且以字母或下划线开头")
        return

    parsed_commands: List[ScheduledCommand] = []
    invalid_commands: List[str] = []

    if args.verbose:
        parsed_commands.append(ScheduledCommand(("echo",), f"开始执行计划任务 {args.name}……"))

    for cmd_str in args.commands:
        cmd, current_arg = CommandManager().parse_command(session.bot, cmd_str)
        if cmd:
            tmp_session = CommandSession(
                session.bot, session.event, cmd, current_arg=current_arg
            )
            if await cmd.run(tmp_session, dry=True):
                parsed_commands.append(ScheduledCommand(cmd.name, current_arg))
                continue
        invalid_commands.append(cmd_str)
    if invalid_commands:
        invalid_commands_joined = "\n".join([f"- {c}" for c in invalid_commands])
        await session.send(
            f"计划任务添加失败，"
            f"因为下面的 {len(invalid_commands)} 个命令无法被运行"
            f"（命令不存在或权限不够）：\n"
            f"{invalid_commands_joined}"
        )
        return

    trigger_args = {
        k: v
        for k, v in args.__dict__.items()
        if k in {"second", "minute", "hour", "day", "month", "day_of_week"}
    }
    try:
        job = await add_scheduled_commands(
            parsed_commands,
            job_id=make_job_id(PLUGIN_NAME, session.event, args.name),
            event=session.event,
            trigger="cron",
            **trigger_args,
            replace_existing=args.force,
        )
    except JobIdConflictError:
        # a job with same name exists
        await session.send(f"计划任务 {args.name} 已存在，" f"若要覆盖请使用 --force 参数")
        return

    await session.send(f"计划任务 {args.name} 添加成功")
    await session.send(format_job(args.name, job))


@cg.command("get")
async def sched_get(session: CommandSession):
    parser = ArgumentParser(session=session, usage=usage.GET)
    parser.add_argument("name")
    args = parser.parse_args(session.argv)
    job = await get_job(make_job_id(PLUGIN_NAME, session.event, args.name))
    if not job:
        await session.send(f"没有找到计划任务 {args.name}，请检查你的输入是否正确")
        return

    await session.send("找到计划任务如下")
    await session.send(format_job(args.name, job))


@cg.command("list")
async def sched_list(session: CommandSession):
    job_id_prefix = make_job_id(PLUGIN_NAME, session.event)
    jobs = await get_jobs(make_job_id(PLUGIN_NAME, session.event))
    if not jobs:
        await session.send("你还没有添加过计划任务")
        return

    for job in jobs:
        await session.send(format_job(job.id[len(job_id_prefix) :], job))
        await asyncio.sleep(0.8)
    await session.send(f"以上是所有的 {len(jobs)} 个计划任务")


@cg.command("remove")
async def sched_remove(session: CommandSession):
    parser = ArgumentParser(session=session, usage=usage.REMOVE)
    parser.add_argument("name")
    args = parser.parse_args(session.argv)
    ok = await remove_job(make_job_id(PLUGIN_NAME, session.event, args.name))
    if ok:
        await session.send(f"成功删除计划任务 {args.name}")
    else:
        await session.send(f"没有找到计划任务 {args.name}，请检查你的输入是否正确")


def format_job(job_name: str, job: Job) -> str:
    commands = get_scheduled_commands_from_job(job)
    commands_str = "\n".join([f"- {cmd.name}，参数：{cmd.current_arg}" for cmd in commands])
    return (
        f"名称：{job_name}\n"
        f"下次触发时间："
        f'{job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
        f"命令：\n"
        f"{commands_str}"
    )
