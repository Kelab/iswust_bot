import hashlib
from typing import List, Optional, Tuple

from ..env import env


def true_ret(data=None, msg="success"):
    return {"code": 200, "data": data, "msg": msg}


def false_ret(data=None, msg="fail", code=-1):
    return {"code": code, "data": data, "msg": msg}


def check_args(**kwargs) -> Tuple[bool, Optional[List[str]]]:
    msg_list = []
    for k, v in kwargs.items():
        if v is None:
            msg = f"Missing arg: {k}"
            msg_list.append(msg)
    if msg_list:
        return False, msg_list
    return True, None


def to_token(_qq) -> str:
    qq: str = str(_qq)
    key = env("SECRET").encode(encoding="utf8")
    inner = hashlib.md5()
    inner.update(qq.encode())
    outer = hashlib.md5()
    outer.update(inner.hexdigest().encode() + key)
    return outer.hexdigest()
