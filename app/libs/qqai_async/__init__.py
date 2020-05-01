import base64
import hashlib
from typing import Optional
from typing import TypedDict
import httpx

from httpx import Response
from urllib import parse
from app.utils.env import env
from loguru import logger


class QQAI_KEY(TypedDict):
    appid: str
    appkey: str


def check_qqai_key() -> Optional[QQAI_KEY]:
    appid = env("QQAI_APPID", None)
    appkey = env("QQAI_APPKEY", None)
    if not appid or not appkey:
        logger.error("未设置 QQAI_APPID 和 QQAI_APPKEY！")
        return None

    return {"appid": appid, "appkey": appkey}


class QQAIClass:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    mediaHeaders = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    api = ""

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    async def get_base64(self, media_param):
        """获取媒体的Base64字符串

        :param media_param 媒体URL或者媒体BufferedReader对象
        """
        if type(media_param) == str:
            async with httpx.AsyncClient() as client:
                media_data = await client.get(
                    media_param, headers=self.mediaHeaders
                ).content
        elif hasattr(media_param, "read"):
            media_data = await media_param.read()
        else:
            raise TypeError("media must be URL or BufferedReader")

        media = base64.b64encode(media_data).decode("utf-8")
        return media

    def get_sign(self, params):
        """获取签名
        """
        uri_str = ""
        for key in sorted(params.keys()):
            uri_str += "{}={}&".format(key, parse.quote_plus(str(params[key]), safe=""))
        sign_str = uri_str + "app_key=" + self.app_key

        hash_str = hashlib.md5(sign_str.encode("utf-8"))
        return hash_str.hexdigest().upper()

    async def call_api(self, params, api=None) -> Response:
        if api is None:
            api = self.api

        async with httpx.AsyncClient() as client:
            return await client.post(
                api, data=parse.urlencode(params).encode("utf-8"), headers=self.headers
            )
