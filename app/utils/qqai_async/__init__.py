import base64
import hashlib
import json
import time

from urllib import parse

from app.aio import requests


class QQAIClass:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    mediaHeaders = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    async def get_base64(self, media_param):
        """获取媒体的Base64字符串

        :param media_param 媒体URL或者媒体BufferedReader对象
        """
        if type(media_param) == str:
            media_data = await requests.get(media_param,
                                            headers=self.mediaHeaders).content
        elif hasattr(media_param, "read"):
            media_data = media_param.read()
        else:
            raise TypeError("media must be URL or BufferedReader")

        media = base64.b64encode(media_data).decode("utf-8")
        return media

    def get_sign(self, params):
        """获取签名
        """
        uri_str = ""
        for key in sorted(params.keys()):
            uri_str += "{}={}&".format(
                key, parse.quote_plus(str(params[key]), safe=""))
        sign_str = uri_str + "app_key=" + self.app_key

        hash_str = hashlib.md5(sign_str.encode("utf-8"))
        return hash_str.hexdigest().upper()

    async def call_api(self, params, api=None):
        if api is None:
            api = self.api
        return await requests.post(
            api,
            data=parse.urlencode(params).encode("utf-8"),
            headers=self.headers)
