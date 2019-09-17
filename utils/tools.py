import os
import re
import hashlib

from typing import Optional, List, Tuple

from utils.aio import requests
from requests import Response

from log import IS_LOGGER

isUrl = re.compile(r"^https?:\/\/")

encrypt_key = ''

_key: Optional[str] = os.environ.get("ENCRYPT_KEY")
if isinstance(_key, str):
    encrypt_key = int(_key)
else:
    IS_LOGGER.error('ENCRYPT_KEY is not found!')
    raise ValueError("ENCRYPT_KEY is not found!")

IS_LOGGER.info(f"encrypt_key is {encrypt_key}")
tcn_source = os.environ.get("T_CN_SOURCE")


def bot_hash(message: str) -> str:
    message = str(message)
    key = os.environ.get("ENCRYPT_KEY") or 'qq_bot_is_so_niu_bi'
    key = key.encode()
    inner = hashlib.md5()
    inner.update(message.encode())
    outer = hashlib.md5()
    outer.update(inner.hexdigest().encode() + key)
    return outer.hexdigest()


async def dwz(url: str) -> Optional[str]:
    if not isUrl.match(url):
        IS_LOGGER.error('请输入正常的 url')
        return None

    dwz_url = "http://sa.sogou.com/gettiny?={}"

    data = {
        "url": url,
    }
    r: Response = await requests.get(dwz_url, params=data)
    res = await r.text

    return res


def check_args(**kwargs) -> Tuple[bool, Optional[List[str]]]:
    msg_list = []
    for k, v in kwargs.items():
        if v is None:
            msg = f"Missing arg: {k}"
            msg_list.append(msg)
    if msg_list:
        return False, msg_list
    return True, None
