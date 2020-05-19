import asyncio
from typing import List
from loguru import logger
from nonebot import get_bot
from nonebot.command import call_command, _FinishException

from app.env import env
from app.models.subscribe import SubUser

PREFIX = "r"
rsshub_url: str = env("RSSHUB_URL", "").rstrip("/")
rss_info = {
    "教务处新闻": "/swust/jwc/news",
    "教务处通知 创新创业教育": "/swust/jwc/notice/1",
    "教务处通知 学生学业": "/swust/jwc/notice/2",
    "教务处通知 建设与改革": "/swust/jwc/notice/3",
    "教务处通知 教学质量保障": "/swust/jwc/notice/4",
    "教务处通知 教学运行": "/swust/jwc/notice/5",
    "教务处通知 教师教学": "/swust/jwc/notice/6",
    "计科学院通知 新闻动态": "/swust/cs/1",
    "计科学院通知 学术动态": "/swust/cs/2",
    "计科学院通知 通知公告": "/swust/cs/3",
    "计科学院通知 教研动态": "/swust/cs/4",
}


def get_rss_list():
    msg = PREFIX + f"0. `{PREFIX}系列` 所有\n"
    for idx, key in enumerate(rss_info.keys()):
        msg = msg + f"{PREFIX}{idx+1}. {key}\n"

    return msg


def make_url(idx: int) -> List[str]:
    if idx >= len(rss_info) or 0 > idx:
        return []
    if idx == 0:
        url = [rsshub_url + u for u in list(rss_info.values())]
    else:
        _url = rss_info[list(rss_info.keys())[idx - 1]]
        url = [rsshub_url + _url]
    return url


async def handle_school_notice(event, msg: str):
    if msg.startswith(PREFIX):
        bot = get_bot()
        idx = msg.replace(PREFIX, "")
        urls = make_url(int(idx))
        if urls:
            await asyncio.gather(
                *[
                    call_command(
                        bot,
                        event,
                        ("rss", "add"),
                        args={"url": url},
                        disable_interaction=True,
                    )
                    for url in urls
                ]
            )
        else:
            await bot.send(event, "序号不存在")
        raise _FinishException


async def handle_get_notices(event):
    result = {}
    subs = await SubUser.get_user_subs(event)
    if subs:
        result[f"{PREFIX}0"] = f"`{PREFIX}系列` 所有"
        for idx, sub in enumerate(subs):
            result[f"{PREFIX}{idx+1}"] = sub.sub_content.name
    return result


async def rm_sub(event, sub):
    bot = get_bot()
    try:
        await SubUser.remove_sub(event, sub.link)
        await bot.send(event, f"{sub.sub_content.name} 删除成功")
    except Exception as e:
        logger.exception(e)
        await bot.send(event, "出了点问题，请稍后再试吧")


async def handle_rm_notice(event, idx):
    if idx.startswith(PREFIX):
        bot = get_bot()
        idx = idx.replace(PREFIX, "")
        if idx.isdigit():
            subs = await SubUser.get_user_subs(event)
            idx = int(idx)  # type: ignore
            if idx == 0:  # 删除所有
                await asyncio.wait([rm_sub(event, sub) for sub in subs])
                return
            idx = idx - 1
            if not (0 <= idx < len(subs)):
                await bot.send(event, "没有找到你输入的序号哦")

            sub = subs[idx]
            await rm_sub(event, sub)
        else:
            await bot.send(event, "序号不存在")
        raise _FinishException
