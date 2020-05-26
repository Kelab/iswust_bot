from typing import Dict, Optional

from aiocqhttp import Event
from loguru import logger
from nonebot.command import _FinishException, call_command

from app.env import env
from app.models.subscribe import SubUser

from . import BaseSub


class SchoolNoticeSub(BaseSub):
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

    dct = {PREFIX + str(idx): k for idx, k in enumerate(rss_info.keys())}
    inv_dct = {v: k for k, v in dct.items()}

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        return cls.dct

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        subs = await SubUser.get_user_subs(event)
        if subs:
            for sub in subs:
                name = sub.sub_content.name
                key = cls.inv_dct.get(name)
                if not key:
                    continue
                result[key] = name
        return result

    @classmethod
    async def del_sub(cls, event: Event, key: str):
        if key.startswith(cls.PREFIX):
            name = cls.dct.get(key)
            if name:
                subs = await SubUser.get_user_subs(event)
                for sub in subs:
                    if sub.sub_content.name == name:
                        await cls.rm_sub(event, sub)
                        break
            else:
                await cls.bot.send(event, "没有找到你输入的序号哦")
            raise _FinishException

    @classmethod
    def _make_url(cls, key: str) -> Optional[str]:
        _url = cls.dct.get(key)
        if _url:
            return cls.rsshub_url + _url
        return None

    @classmethod
    async def add_sub(cls, event: Event, key: str):
        if key.startswith(cls.PREFIX):
            url = cls._make_url(key)
            if url:
                await call_command(
                    cls.bot,
                    event,
                    ("rss", "add"),
                    args={"url": url},
                    disable_interaction=True,
                )
            else:
                await cls.bot.send(event, "序号不存在")
            raise _FinishException

    @classmethod
    async def rm_sub(cls, event, sub):
        try:
            await SubUser.remove_sub(event, sub.link)
            await cls.bot.send(event, f"{sub.sub_content.name} 删除成功")
        except Exception as e:
            logger.exception(e)
            await cls.bot.send(event, "出了点问题，请稍后再试吧")
