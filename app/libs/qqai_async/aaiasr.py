import json
import time
import os
from pathlib import Path
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


appid = os.environ.get("QQAI_APPID")
appkey = os.environ.get("QQAI_APPKEY")
coolq_dir = os.environ.get("COOLQ_DIR")
if not appid or not appkey:
    print("未设置 QQAI_APPID 和 QQAI_APPKEY！")
    exit(1)
if not coolq_dir:
    print("未设置 COOLQ_DIR！")
    exit(1)

audio_rec = AudioRecognitionEcho(appid, appkey)
record_dir = Path(coolq_dir) / Path("data/record")


async def echo(silk_fimename: str, coolq_record_dir=record_dir):
    """[echo 语音识别]
    {
        "ret": 0,
        "msg": "ok",
        "data": {
            "format": 2,
            "rate": 16000,
            "text": "今天天气怎么样"
        }
    }
    """
    if not silk_fimename.endswith(".silk"):
        return
    SLIK = 4
    path: Path = coolq_record_dir / silk_fimename

    with path.open(mode="rb") as f:
        result: dict = await audio_rec.run(audio_format=SLIK, speech=f)
    print(result)
    if int(result.get("ret")) == 0:
        return True, result["data"].get("text")
    else:
        return False, result.get("msg")
