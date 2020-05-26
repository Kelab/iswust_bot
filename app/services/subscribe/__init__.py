from abc import ABC
from typing import Dict
from aiocqhttp import Event

from nonebot import get_bot


class BaseSub(ABC):
    bot = get_bot()

    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        ...

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        ...

    @classmethod
    async def del_sub(cls, event: Event, key: str):
        ...

    @classmethod
    async def add_sub(cls, event: Event, key: str):
        ...
