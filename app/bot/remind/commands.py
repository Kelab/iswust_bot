import asyncio
import regex as re
import string
from datetime import datetime
from typing import List

from aiocqhttp import Event as CQEvent
from apscheduler.job import Job
from chinese_time_nlp import TimeNormalizer
from nonebot import CommandGroup, CommandSession, get_bot, on_command
from nonebot import permission as perm
from nonebot.command import CommandManager, call_command
from nonebot.command.argfilter import controllers, extractors, validators
from nonebot.helpers import render_expression

from app.libs.scheduler import add_job, get_jobs, make_job_id, remove_job
from app.libs.scheduler.command import (
    ScheduledCommand,
    add_scheduled_commands,
    get_scheduled_commands_from_job,
)
from app.libs.scheduler.exception import JobIdConflictError
from app.utils.str_ import random_string

from . import EXPR_COULD_NOT, EXPR_OK, EXPR_REMIND

PLUGIN_NAME = "remind"


async def remind(target: str, event: CQEvent):
    """Send shake and remind notification to user

    Args:
        target (str): Thing to remind
        event (CQEvent): Message event
    """
    bot = get_bot()
    # 发送戳一戳
    await bot.send_private_msg(
        self_id=event["self_id"], user_id=event["user_id"], message="[CQ:shake]"
    )
    # 发送提醒
    await bot.send_private_msg(
        self_id=event["self_id"],
        user_id=event["user_id"],
        message=render_expression(EXPR_REMIND, action=target, escape_args=False),
    )


@on_command("_alarm")
async def alarm(session: CommandSession):
    time: datetime = session.get("time")
    target: str = session.get("target")

    # 过滤时间
    now = datetime.now()
    # 过去的时间
    if time <= now:
        session.finish(render_expression(EXPR_COULD_NOT))

    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    await add_job(
        remind,
        trigger="date",
        run_date=time,
        id=make_job_id(
            PLUGIN_NAME,
            session.event,
            (
                random_string(1, string.ascii_lowercase)
                + random_string(7, string.ascii_lowercase + string.digits)
            ),
        ),
        args=[target, session.event],
    )
    cmd, current_arg = CommandManager().parse_command(session.bot, target)
    if cmd:
        tmp_session = CommandSession(
            session.bot, session.event, cmd, current_arg=current_arg
        )
        if await cmd.run(tmp_session, dry=True):
            await add_scheduled_commands(
                ScheduledCommand(cmd.name, current_arg),
                job_id=make_job_id(
                    PLUGIN_NAME,
                    session.event,
                    (
                        random_string(1, string.ascii_lowercase)
                        + random_string(7, string.ascii_lowercase + string.digits)
                    ),
                ),
                event=session.event,
                trigger="date",
                run_date=time,
                replace_existing=True,
            )

    session.finish(
        render_expression(EXPR_OK, time=time_str, action=target, escape_args=False)
        + f"\n提醒创建成功：\n"
        f"> 提醒时间：{time_str}\n"
        f"> 内容：{target}"
    )


cg = CommandGroup(
    PLUGIN_NAME, permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
)


@cg.command(PLUGIN_NAME, aliases=["添加提醒", "新增提醒", "新建提醒"], only_to_me=False)
async def push(session: CommandSession):
    message = session.get(
        "message",
        prompt="你想让我提醒什么内容呢？语句命令都可，输入 `取消、不` 等来取消",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )
    tn = TimeNormalizer()
    hour = session.state.get("hour")
    minute = session.state.get("minute")
    if hour is None or minute is None:
        time = session.get(
            "time",
            prompt="你希望我在每天的什么时候给你提醒呢？\n",
            arg_filters=[
                controllers.handle_cancellation(session),
                str.lstrip,
                validators.not_empty("请输入有效内容哦～"),
            ],
        )
        m = re.match(r"(\d{1,2})[.:：](\d{1,2})", time)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2) or 0)
        else:
            time_json = tn.parse(time)
            if time_json["type"] == "error":
                del session.state["time"]
                session.pause("时间格式不对啦，请重新发送")
            elif time_json["type"] == "timedelta":
                time_diff = time_json["timedelta"]
                hour = time_diff["hour"]
                minute = time_diff["minute"]
            elif time_json["type"] == "timestamp":
                time_target = datetime.strptime(
                    time_json["timestamp"], "%Y-%m-%d %H:%M:%S"
                )
                # 默认时间点为中午12点
                if (
                    not re.search(r"[\d+一二两三四五六七八九十]+点", time)
                    and time_target.hour == 0
                    and time_target.minute == 0
                    and time_target.second == 0
                ):
                    time_target.replace(hour=12)
                hour = time_target.hour
                minute = time_target.minute

    session.state["hour"] = hour
    session.state["minute"] = minute
    escaped_message = message.replace("\\", "\\\\").replace('"', '\\"')
    switch_arg = f'--repeat "{escaped_message}"'

    try:
        job = await add_scheduled_commands(
            ScheduledCommand("switch", switch_arg),
            job_id=make_job_id(
                PLUGIN_NAME,
                session.ctx,
                (
                    random_string(1, string.ascii_lowercase)
                    + random_string(7, string.ascii_lowercase + string.digits)
                ),
            ),
            event=session.event,
            trigger="cron",
            hour=hour,
            minute=minute,
            replace_existing=False,
        )
        session.finish(
            f"添加提醒成功啦，下次提醒时间 " f'{job.next_run_time.strftime("%Y-%m-%d %H:%M")}'
        )
    except JobIdConflictError:
        session.finish("添加提醒失败，有可能只是运气不好哦，请稍后重试～")


@push.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


@cg.command("show", aliases=["查看提醒", "我的提醒", "提醒列表"], only_to_me=False)
async def _(session: CommandSession):
    jobs = session.state.get("jobs") or await get_push_jobs(session.event)

    if not jobs:
        session.finish("你还没有添加任何提醒哦")

    for i, job in enumerate(jobs):
        await session.send(format_subscription(i + 1, job))
        await asyncio.sleep(0.2)
    session.finish(f"以上是所有的 {len(jobs)} 个提醒")


@cg.command("rm", aliases=["取消提醒", "停止提醒", "关闭提醒", "删除提醒"], only_to_me=False)
async def rm(session: CommandSession):
    jobs = session.state.get("jobs") or await get_push_jobs(session.event)
    index = session.state.get("index")
    if index is None:
        session.state["jobs"] = jobs
        await call_command(
            session.bot,
            session.ctx,
            (PLUGIN_NAME, "show"),
            args={"jobs": jobs},
            disable_interaction=True,
        )
        if not jobs:
            session.finish()

        index = session.get(
            "index",
            prompt="你想取消哪一个提醒呢？（请发送序号）",
            arg_filters=[
                extractors.extract_text,
                controllers.handle_cancellation(session),
                validators.ensure_true(str.isdigit, "请输入序号哦～"),
                int,
            ],
        )

    index = index - 1
    if not (0 <= index < len(jobs)):
        session.finish("没有找到你输入的序号哦")

    job = jobs[index]
    if await remove_job(job.id):
        session.finish("取消提醒成功")
    else:
        session.finish("出了点问题，请稍后再试吧")


@rm.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            try:
                session.state["index"] = int(session.current_arg)
            except Exception:
                pass
        return


async def get_push_jobs(event) -> List[Job]:
    return await get_jobs(make_job_id(PLUGIN_NAME, event))


def format_subscription(index: int, job: Job) -> str:
    command = get_scheduled_commands_from_job(job)[0]
    switch_argument = command.current_arg
    message = switch_argument[switch_argument.find('"') + 1 : -1]
    message = message.replace('\\"', '"').replace("\\\\", "\\")
    return (
        f"序号：{index}\n"
        f"下次提醒时间："
        f'{job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
        f"提醒内容："
        f"{message}"
    )
