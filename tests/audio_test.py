import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

sys.path.append(str(Path('.').resolve()))
from utils.qqai.aaiasr import rec_silk
filename = "777D935D643B0300777D935D643B0300.silk"


@pytest.mark.asyncio
async def test_app():
    text = await rec_silk(filename, Path('./tests/assets/record').resolve())
    assert text == "明天课表"
