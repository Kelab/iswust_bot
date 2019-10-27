import json
import time

from . import QQAIClass


class AudioRecognitionEcho(QQAIClass):
    """语音识别-echo版"""

    api = "https://api.ai.qq.com/fcgi-bin/aai/aai_asr"

    async def make_params(self, audio_format: int, speech, rate=None):
        """获取调用接口的参数"""
        params = {
            "app_id": self.app_id,
            "time_stamp": int(time.time()),
            "nonce_str": int(time.time()),
            "format": audio_format,
            "speech": await self.get_base64(speech),
            "rate": rate or 16000,
        }

        params["sign"] = self.get_sign(params)
        return params

    async def run(self, audio_format, speech, rate=None):
        params = await self.make_params(audio_format, speech, rate)
        response = await self.call_api(params)
        result = json.loads(await response.text)
        return result
