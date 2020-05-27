from typing import Dict

from aiocqhttp import Event
from nonebot import get_bot

from .dean import DeanSub
from .school_notice import SchoolNoticeSub


def judge_sub(key: str):
    if key.startswith(DeanSub.PREFIX):
        return DeanSub
    if key.startswith(SchoolNoticeSub.PREFIX):
        return SchoolNoticeSub


class SubWrapper:
    bot = get_bot()

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        result = {}
        result.update(SchoolNoticeSub.get_subs())
        result.update(DeanSub.get_subs())
        return result

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        result.update(await SchoolNoticeSub.get_user_sub(event))
        result.update(await DeanSub.get_user_sub(event))
        return result
