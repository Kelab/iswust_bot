import hashlib
import re
from typing import List, Optional, Tuple

import httpx
from loguru import logger
from werkzeug.utils import find_modules, import_string

from ..env import env

isUrl = re.compile(r"^https?:\/\/")


def bot_hash(message: str) -> str:
    message = str(message)
    key = env("SECRET").encode(encoding="utf8")
    inner = hashlib.md5()
    inner.update(message.encode())
    outer = hashlib.md5()
    outer.update(inner.hexdigest().encode() + key)
    return outer.hexdigest()


async def dwz(url: str) -> Optional[str]:
    if not isUrl.match(url):
        logger.error("请输入正常的 url")
        raise ValueError("请输入正常的 url")

    dwz_url = "http://sa.sogou.com/gettiny?={}"

    data = {"url": url}
    async with httpx.AsyncClient() as client:
        r: httpx.Response = await client.get(dwz_url, params=data)
        return r.text


def check_args(**kwargs) -> Tuple[bool, Optional[List[str]]]:
    msg_list = []
    for k, v in kwargs.items():
        if v is None:
            msg = f"Missing arg: {k}"
            msg_list.append(msg)
    if msg_list:
        return False, msg_list
    return True, None


def load_modules(path):
    """引入路径下所有包
    """
    for model in find_modules(path):
        try:
            import_string(model)
            logger.info(f'Load model: "{model}"')
        except Exception as e:
            logger.error(f'Failed to Load "{model}", error: {e}')
            logger.exception(e)
