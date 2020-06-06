from abc import ABC
from typing import Dict
from aiocqhttp import Event


class BaseSub(ABC):
    PREFIX = ""
    sub_info = {}

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

    @classmethod
    def dct(cls) -> Dict[str, str]:
        """
        { "s0":"有新成绩出来时提醒我", "s1":"有新考试出来提醒我" }
        """
        dct = {f"{cls.PREFIX}{idx}": k for idx, k in enumerate(cls.sub_info.keys())}
        return dct

    @classmethod
    def inv_dct(cls) -> Dict[str, str]:
        """
        { "有新成绩出来时提醒我":"s0", "有新考试出来提醒我":"s1" }
        """
        return {v: k for k, v in cls.dct().items()}
