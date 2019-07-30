import os
import requests

key_ = int(os.environ.get("KEY"))
tcn_source = os.environ.get("T_CN_SOURCE")


def xor_encrypt(num: str, key: int = key_):
    try:
        num = int(num)
    except TypeError:
        pass
    return num ^ key


def xor_decrypt(token: int, key: int = key_):
    try:
        token = int(token)
    except TypeError:
        pass
    return token ^ key


def tcn(url):
    # 接口： https://open.weibo.com/wiki/2/short_url/shorten
    # http://jump.sinaapp.com/api.php?url_long=
    tcn_url = "http://api.t.sina.com.cn/short_url/shorten.json"
    tcn_source = os.environ.get("T_CN_SOURCE")

    for source in [tcn_source]:
        data = {
            "source": source,
            "url_long": url,
        }
        r = requests.get(tcn_url, params=data)
        r = r.json()

        if isinstance(r, list):
            return r[0]['url_short']

    return None
