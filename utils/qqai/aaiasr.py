import os
import sys
from pathlib import Path
from utils.qqai import AudioRecognitionEcho

appid = os.environ.get("QQAI_APPID")
appkey = os.environ.get("QQAI_APPKEY")
if not appid or not appkey:
    print("未找到 appid appkey")
    exit(1)

audio_rec = AudioRecognitionEcho(appid, appkey)


async def rec_silk(silk_fimename: str,
                   coolq_record_dir=Path('/home/artin/coolq/data/record')):
    """[语音识别]
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
    if not silk_fimename.endswith('.silk'):
        return
    SLIK = 4
    path: Path = coolq_record_dir / silk_fimename

    with path.open(mode="rb") as f:
        result: dict = await audio_rec.run(audio_format=SLIK, speech=f)
    print(result)
    if int(result.get('ret')) == 0:
        return result.get('data').get('text')
    else:
        return result.get('msg')
