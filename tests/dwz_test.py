import pytest


@pytest.mark.asyncio
async def test_dwz():
    from app.utils.tools import dwz

    shorten_url_ = await dwz("https://www.baidu.com")
    assert shorten_url_ == "https://url.cn/5NzSyLv"
