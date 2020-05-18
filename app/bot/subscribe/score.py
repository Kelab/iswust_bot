from loguru import logger
from nonebot import get_bot
from nonebot.command import _FinishException
from app.libs.scheduler import get_job, make_job_id, remove_job, add_job
from apscheduler.triggers.interval import IntervalTrigger

PLUGIN_NAME = "sub_score_update"
PREFIX = "s"

lst = ["有新成绩出来时提醒我"]


def get_score_subscribes():
    msg = ""
    for idx, v in enumerate(lst):
        msg = msg + PREFIX + f"{idx}. {v}\n"
    return msg


async def handle_subscribe_score(event, msg: str):
    if msg.startswith(PREFIX):
        bot = get_bot()
        try:
            idx = int(msg.replace(PREFIX, ""))
            if idx == 0:
                # 添加任务
                await add_job(
                    func=check_update,
                    trigger=IntervalTrigger(minutes=10, jitter=10),
                    args=(event,),
                    id=make_job_id(PLUGIN_NAME, event),
                    misfire_grace_time=60,
                    job_defaults={"max_instances": 10},
                )
                await bot.send(event, "添加成功！")
        except Exception as e:
            await bot.send(event, "输入有误")
            logger.exception(e)
        raise _FinishException


async def check_update(event):
    logger.info(event)


async def handle_get_scores(event):
    result = {}
    job = await get_job(make_job_id(PLUGIN_NAME, event))
    if job:
        result[f"{PREFIX}0"] = lst[0]
    return result


async def handle_rm_score(event, idx):
    if idx.startswith(PREFIX):
        bot = get_bot()
        idx = idx.replace(PREFIX, "")
        if idx.isdigit():
            idx = int(idx)  # type: ignore
            if idx == 0:
                res = await remove_job(make_job_id(PLUGIN_NAME, event))
                if res:
                    await bot.send(event, f"删除 `{lst[0]}` 成功")
                else:
                    await bot.send(event, "删除失败，请稍后再试")
        else:
            await bot.send(event, "序号不存在")
        raise _FinishException
