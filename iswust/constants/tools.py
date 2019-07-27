import os
import requests
key_ = int(os.environ.get("KEY"))


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


def unu(url, action="shorturl", format_="simple", keyword=""):
    unu_url = "https://u.nu/api.php"
    data = {
        "action": action,
        "format": format_,
        "url": url,
        "keyword": keyword
    }
    r = requests.get(unu_url, params=data)
    return r.text
