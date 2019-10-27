import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(".").resolve()))
from app.utils.asr_rec import echo

filename = "777D935D643B0300777D935D643B0300.silk"


@pytest.mark.asyncio
async def test_echo():
    result, text = await echo(filename,
                              Path("./tests/assets/record").resolve())
    assert text == "明天课表"
    assert result is True


@pytest.mark.asyncio
async def test_app1():
    result, text = await echo(filename,
                              Path("./tests/assets/record").resolve())
    assert text == "明天课表"
    assert result is True
