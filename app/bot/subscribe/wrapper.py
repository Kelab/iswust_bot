from .school_notice import handle_school_notice, handle_get_notices, handle_rm_notice
from .score import handle_subscribe_score, handle_get_scores, handle_rm_score
from nonebot.command import _FinishException

from loguru import logger


async def handle_message(event, message):
    try:
        await handle_school_notice(event, message)
        await handle_subscribe_score(event, message)
    except _FinishException:
        pass
    except Exception as e:
        logger.exception(e)


async def get_subs(event):
    result = {}
    result.update(await handle_get_notices(event))
    result.update(await handle_get_scores(event))
    return result


async def handle_rm(event, idx):
    try:
        await handle_rm_notice(event, idx)
        await handle_rm_score(event, idx)
    except _FinishException:
        pass
    except Exception as e:
        logger.exception(e)
