import asyncio
import re
import string
from typing import List

from nonebot import CommandSession, CommandGroup
from nonebot import permission as perm
from nonebot.command import call_command
from nonebot.command.argfilter import converters, extractors, validators, controllers

from app.libs import scheduler
from app.libs.scheduler import ScheduledCommand
from app.utils.str_common import random_string

__plugin_name__ = "推送"

PLUGIN_NAME = "push"

cg = CommandGroup(
    PLUGIN_NAME, permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
)


@cg.command("push", aliases=["推送", "添加推送", "新增推送", "新建推送"], only_to_me=False)
async def push(session: CommandSession):
    message = session.get(
        "message",
        prompt="你想让我推送什么内容呢？语句命令都可，输入 `取消、不` 等来取消",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )

    hour = session.state.get("hour")
    minute = session.state.get("minute")
    if hour is None or minute is None:
        time = session.get(
            "time",
            prompt="你希望我在每天的什么时候给你推送呢？\n" "（请使用24小时制，并使用阿拉伯数字表示小时和分钟）",
            arg_filters=[
                controllers.handle_cancellation(session),
                str.lstrip,
                validators.not_empty("请输入有效内容哦～"),
            ],
        )
        m = re.match(r"(?P<hour>\d{1,2})[.:：](?P<minute>\d{1,2})", time)
        if not m:
            m = re.match(
                r"(?P<hour>\d{1,2})\s*[点时]\s*" r"(?:(?P<minute>\d{1,2}|半|一刻)\s*[分]?)?",
                time,
            )

        if m:
            hour = int(m.group("hour"))
            session.state["hour"] = hour
            try:
                minute = int(m.group("minute") or 0)
            except ValueError:
                if m.group("minute") == "半":
                    minute = 30
                elif m.group("minute") == "一刻":
                    minute = 15
            session.state["minute"] = minute
        else:
            del session.state["time"]
            session.pause("时间格式不对啦，请重新发送")

    repeat = session.get(
        "repeat",
        prompt="是否希望我在推送消息的时候重复你上面发的消息内容呢？（请回答是或否）",
        arg_filters=[
            extractors.extract_text,
            converters.simple_chinese_to_bool,
            validators.ensure_true(lambda x: x is not None, "我听不懂呀，请用是或否再回答一次呢"),
        ],
    )

    escaped_message = message.replace("\\", "\\\\").replace('"', '\\"')
    if repeat:
        switch_arg = f'--repeat "{escaped_message}"'
    else:
        switch_arg = f'"{escaped_message}"'

    try:
        job = await scheduler.add_scheduled_commands(
            ScheduledCommand("switch", switch_arg),
            job_id=scheduler.make_job_id(
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
            f"添加推送成功啦，下次推送时间 " f'{job.next_run_time.strftime("%Y-%m-%d %H:%M")}'
        )
    except scheduler.JobIdConflictError:
        session.finish("添加推送失败，有可能只是运气不好哦，请稍后重试～")


@push.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


@cg.command("show", aliases=["查看推送", "我的推送", "推送列表"], only_to_me=False)
async def _(session: CommandSession):
    jobs = session.state.get("jobs") or await get_push_jobs(session.event)

    if not jobs:
        session.finish(f"你还没有添加任何推送哦")

    for i, job in enumerate(jobs):
        await session.send(format_subscription(i + 1, job))
        await asyncio.sleep(0.2)
    session.finish(f"以上是所有的 {len(jobs)} 个推送")


@cg.command("rm", aliases=["取消推送", "停止推送", "关闭推送", "删除推送"], only_to_me=False)
async def rm(session: CommandSession):
    jobs = session.state.get("jobs") or await get_push_jobs(session.event)
    index = session.state.get("index")
    if index is None:
        session.state["jobs"] = jobs
        await call_command(
            session.bot,
            session.ctx,
            ("push", "show"),
            args={"jobs": jobs},
            disable_interaction=True,
        )
        if not jobs:
            session.finish()

        index = session.get(
            "index",
            prompt="你想取消哪一个推送呢？（请发送序号）",
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
    if await scheduler.remove_job(job.id):
        session.finish("取消推送成功")
    else:
        session.finish("出了点问题，请稍后再试吧")


async def get_push_jobs(event) -> List[scheduler.Job]:
    return await scheduler.get_jobs(scheduler.make_job_id(PLUGIN_NAME, event))


def format_subscription(index: int, job: scheduler.Job) -> str:
    command = scheduler.get_scheduled_commands_from_job(job)[0]
    switch_argument = command.current_arg
    message = switch_argument[switch_argument.find('"') + 1 : -1]
    message = message.replace('\\"', '"').replace("\\\\", "\\")
    return (
        f"序号：{index}\n"
        f"下次推送时间："
        f'{job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
        f"推送内容："
        f"{message}"
    )
