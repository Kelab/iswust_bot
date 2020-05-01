import json
import time
from pathlib import Path

import aiofiles
from loguru import logger


from . import QQAIClass, check_qqai_key


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
    key = check_qqai_key()
    if not key:
        return False, "未设置 QQAI 相关密钥"

    audio_rec = AudioRecognitionEcho(key["appid"], key["appkey"])
    if not silk_fimename.endswith(".silk"):
        return False, "没有检测到语音文件"

    if coolq_record_dir is None:
        coolq_record_dir = Path("/coolq") / Path("data/record")

    SLIK = 4
    path: Path = coolq_record_dir / silk_fimename
    async with aiofiles.open(path, mode="rb") as f:
        result: dict = await audio_rec.run(audio_format=SLIK, speech=f)
    logger.info(result)
    if int(result.get("ret", -1)) == 0:
        return True, result["data"].get("text")
    else:
        return False, result.get("msg")
