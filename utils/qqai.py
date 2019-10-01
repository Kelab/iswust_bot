import hashlib
import base64
from urllib import parse
from utils.aio import requests

import time
import json


class QQAIClass:
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    mediaHeaders = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
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
        elif hasattr(media_param, 'read'):
            media_data = media_param.read()
        else:
            raise TypeError('media must be URL or BufferedReader')

        media = base64.b64encode(media_data).decode("utf-8")
        return media

    def get_sign(self, params):
        """获取签名
        """
        uri_str = ''
        for key in sorted(params.keys()):
            uri_str += '{}={}&'.format(
                key, parse.quote_plus(str(params[key]), safe=''))
        sign_str = uri_str + 'app_key=' + self.app_key

        hash_str = hashlib.md5(sign_str.encode('utf-8'))
        return hash_str.hexdigest().upper()

    async def call_api(self, params, api=None):
        if api is None:
            api = self.api
        return await requests.post(
            api,
            data=parse.urlencode(params).encode("utf-8"),
            headers=self.headers)


class AudioRecognitionEcho(QQAIClass):
    """语音识别-echo版"""
    api = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'

    async def make_params(self, audio_format, speech, rate=None):
        """获取调用接口的参数"""
        params = {
            'app_id': self.app_id,
            'time_stamp': int(time.time()),
            'nonce_str': int(time.time()),
            'format': audio_format,
            'speech': await self.get_base64(speech),
            'rate': rate or 16000
        }

        params['sign'] = self.get_sign(params)
        return params

    async def run(self, audio_format, speech, rate=None):
        params = await self.make_params(audio_format, speech, rate)
        response = await self.call_api(params)
        result = json.loads(await response.text)
        return result
