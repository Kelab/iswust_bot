import os
import re
import time
import hashlib

from typing import Optional, List, Tuple

from utils.aio import requests
from requests import Response

from log import IS_LOGGER

isUrl = re.compile(r"^https?:\/\/")


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
        raise ValueError("请输入正常的 url")

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


async def post_msg(ctx, msg: str):
    ctx['time'] = int(time.time())
    ctx['raw_message'] = msg
    ctx['message'] = [{'type': 'text', 'data': {'text': msg}}]

    await requests.post('http://127.0.0.1:8080', ctx)
