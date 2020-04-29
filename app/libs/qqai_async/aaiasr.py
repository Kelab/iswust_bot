import json
import time
import os
from pathlib import Path
from loguru import logger
from . import QQAIClass
from nonebot import get_bot


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
        result = json.loads(response.text)
        return result


appid = os.environ.get("QQAI_APPID")
appkey = os.environ.get("QQAI_APPKEY")

if not appid or not appkey:
    logger.error("未设置 QQAI_APPID 和 QQAI_APPKEY！")


audio_rec = AudioRecognitionEcho(appid, appkey)
record_dir = Path("/coolq") / Path("data/record")


async def echo(silk_fimename: str, coolq_record_dir=None):
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
        return False, "没有检测到语音文件"

    if coolq_record_dir is None:
        coolq_record_dir = record_dir

    SLIK = 4
    path: Path = coolq_record_dir / silk_fimename

    with path.open(mode="rb") as f:
        result: dict = await audio_rec.run(audio_format=SLIK, speech=f)
    logger.info(result)
    if int(result.get("ret", -1)) == 0:
        return True, result["data"].get("text")
    else:
        return False, result.get("msg")
