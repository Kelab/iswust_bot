from loguru import logger
from nonebot.command import _FinishException

from typing import Dict
from aiocqhttp import Event

from .school_notice import SchoolNoticeSub
from .score import ScoreSub
from . import BaseSub


class SubWrapper(BaseSub):
    @classmethod
    def get_subs(cls) -> Dict[str, str]:
        result = {}
        result.update(SchoolNoticeSub.get_subs())
        result.update(ScoreSub.get_subs())
        return result

    @classmethod
    async def get_user_sub(cls, event: Event) -> dict:
        result = {}
        result.update(await SchoolNoticeSub.get_user_sub(event))
        result.update(await ScoreSub.get_user_sub(event))
        return result

    @classmethod
    async def del_sub(cls, event: Event, key: str) -> bool:
        try:
            await SchoolNoticeSub.del_sub(event, key)
            await ScoreSub.del_sub(event, key)
            # 上面处理成功后已经 raise 了 _FinishException
            await cls.bot.send(event, "序号不存在")
            return False
        except _FinishException:
            return True
        except Exception as e:
            logger.exception(e)
            return False

    @classmethod
    async def add_sub(cls, event: Event, key: str) -> bool:
        try:
            await SchoolNoticeSub.add_sub(event, key)
            await ScoreSub.add_sub(event, key)
            # 上面处理成功后已经 raise 了 _FinishException
            await cls.bot.send(event, "序号不存在")
            return False
        except _FinishException:
            return True
        except Exception as e:
            logger.exception(e)
            return False
