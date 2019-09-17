import re

from typing import Optional

import requests
from requests import Response

isUrl = re.compile(r"^https?:\/\/")


def tcn(url: str) -> Optional[str]:
    if not isUrl.match(url):
        return None
    dwz_url = "http://sa.sogou.com/gettiny?={}"

    data = {
        "url": url,
    }
    r: Response = requests.get(dwz_url, params=data)

    return r.text


def test_tcn1():
    shorten_url_ = tcn('https://www.baidu.com')
    assert shorten_url_ == 'https://url.cn/5NzSyLv'
