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

from .rsshub_wrapper import get_rss_list, make_url

__plugin_name__ = "通知"

PLUGIN_NAME = "subscribe"

cg = CommandGroup(
    "subscribe", permission=perm.PRIVATE | perm.GROUP_ADMIN | perm.DISCUSS
)


@cg.command("subscribe", aliases=["订阅", "添加订阅", "新增订阅", "新建订阅"], only_to_me=False)
async def subscribe(session: CommandSession):
    message = session.get(
        "message",
        prompt=f"你想订阅什么内容呢，请输入序号？（可输入 `取消、不` 等取消）：\n{get_rss_list()}",
        arg_filters=[
            controllers.handle_cancellation(session),
            str.lstrip,
            validators.not_empty("请输入有效内容哦～"),
        ],
    )

    try:
        urls = make_url(int(message))
        await asyncio.gather(
            *[
                await call_command(
                    session.bot,
                    session.ctx,
                    ("rss", "add"),
                    args={"url": url},
                    disable_interaction=True,
                )
                for url in urls
            ]
        )

    except scheduler.JobIdConflictError:
        session.finish("订阅失败，有可能只是运气不好哦，请稍后重试～")


@subscribe.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        if session.current_arg:
            session.state["message"] = session.current_arg
        return


@cg.command("show", aliases=["查看订阅", "我的订阅"], only_to_me=False)
async def _(session: CommandSession):
    jobs = session.state.get("jobs") or await get_subscriptions(session.ctx)

    if not jobs:
        session.finish(f"你还没有订阅任何内容哦")

    for i, job in enumerate(jobs):
        await session.send(format_subscription(i + 1, job))
        await asyncio.sleep(0.2)
    session.finish(f"以上是所有的 {len(jobs)} 个订阅")


@cg.command("unsubscribe", aliases=["取消订阅", "停止订阅", "关闭订阅", "删除订阅"], only_to_me=False)
async def unsubscribe(session: CommandSession):
    jobs = session.state.get("jobs") or await get_subscriptions(session.event)
    index = session.state.get("index")
    if index is None:
        session.state["jobs"] = jobs
        await call_command(
            session.bot,
            session.ctx,
            ("subscribe", "show"),
            args={"jobs": jobs},
            disable_interaction=True,
        )
        if not jobs:
            session.finish()

        index = session.get(
            "index",
            prompt="你想取消哪一个订阅呢？（请发送序号）",
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
        session.finish("取消订阅成功")
    else:
        session.finish("出了点问题，请稍后再试吧")


async def get_subscriptions(event) -> List[scheduler.Job]:
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
        f"订阅内容："
        f"{message}"
    )
