import os
import re
import requests
from typing import Optional

from log import IS_LOGGER

isUrl = re.compile(r"^https?:\/\/")

encrypt_key = ''

_key: Optional[str] = os.environ.get("ENCRYPT_KEY")
if isinstance(_key, str):
    encrypt_key = int(_key)
else:
    IS_LOGGER.error('ENCRYPT_KEY is not found!')
    raise ValueError("ENCRYPT_KEY is not found!")

tcn_source = os.environ.get("T_CN_SOURCE")


def xor_encrypt(num: int, key: int = encrypt_key):
    try:
        num = int(num)
    except TypeError:
        IS_LOGGER.error(f'num: {num}, encrypt_key: {key}')
    return num ^ key


def xor_decrypt(token: int, key: int = encrypt_key):
    try:
        token = int(token)
    except TypeError:
        IS_LOGGER.error(f'token: {token}, encrypt_key: {key}')
    return token ^ key


def tcn(url: str) -> Optional[str]:
    if not isUrl.match(url):
        IS_LOGGER.error('请输入正常的 url')
        return None

    # 接口： https://open.weibo.com/wiki/2/short_url/shorten
    tcn_url = "http://api.t.sina.com.cn/short_url/shorten.json"
    tcn_source = os.environ.get("T_CN_SOURCE")

    data = {
        "source": tcn_source,
        "url_long": url,
    }
    r = requests.get(tcn_url, params=data)
    r = r.json()

    if isinstance(r, list):
        return r[0]['url_short']

    return None
