import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(".").resolve()))
import os

filename = "777D935D643B0300777D935D643B0300.silk"


@pytest.mark.asyncio
async def test_echo():
    os.environ["COOLQ_DIR"] = "tests"
    from app.libs.qqai_async.aaiasr import echo

    # 接口十分不稳定 无法测试
    result, text = await echo(filename)
    assert text in ["明天课表", "system busy, please try again later"]
    # assert False, "dumb assert to make PyTest print my stuff"
