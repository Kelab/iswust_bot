import os
from pathlib import Path

from .qqai_async.aaiasr import AudioRecognitionEcho

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
