from typing import Dict, Optional, Tuple

from aiocqhttp import Event
from nonebot import get_bot
from nonebot.command import call_command

from app.env import env
from app.models.subscribe import SubUser

from . import BaseSub

rsshub_url: str = env("RSSHUB_URL", "").rstrip("/")


class SchoolNoticeSub(BaseSub):
    PREFIX = "r"
    sub_info = {
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
    inv_sub_info = {v: k for k, v in sub_info.items()}

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        return cls.dct()

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        subs = await SubUser.get_user_subs(event)
        if subs:
            for sub in subs:
                link = sub.link.replace(rsshub_url, "")
                name = cls.inv_sub_info.get(link, "")
                key = cls.inv_dct().get(name)
                if not key:
                    continue
                result[key] = name
        return result

    @classmethod
    async def del_sub(cls, event: Event, key: str) -> Tuple[bool, str]:
        try:
            name = cls.dct().get(key, "")
            link = cls.sub_info.get(name)
            subs = await SubUser.get_user_subs(event)
            for sub in subs:
                sub_link = sub.link.replace(rsshub_url, "")
                if sub_link == link:
                    await SubUser.remove_sub(event, sub.link)
                    return True, f"{sub.sub_content.name} 删除成功"
            return False, "你没有这个订阅哦"
        except Exception:
            return False, "出了点问题，请稍后再试吧"

    @classmethod
    def _make_url(cls, key: str) -> Optional[str]:
        name = cls.dct().get(key, "")
        _url = cls.sub_info.get(name)
        if _url:
            return rsshub_url + _url
        return None

    @classmethod
    async def add_sub(cls, event: Event, key: str) -> Tuple[bool, str]:
        url = cls._make_url(key)
        name = cls.dct().get(key, "")
        if url:
            await call_command(
                get_bot(),
                event,
                ("rss", "add"),
                args={"url": url, "silent": True},
                disable_interaction=True,
            )
            return True, f"订阅 {name} 成功"
        else:
            return False, "序号不存在"
