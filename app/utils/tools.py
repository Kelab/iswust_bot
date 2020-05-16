import re
from typing import Optional

import httpx
from loguru import logger
from werkzeug.utils import find_modules, import_string


isUrl = re.compile(r"^https?:\/\/")


async def dwz(url: str) -> Optional[str]:
    if not isUrl.match(url):
        logger.error("请输入正常的 url")
        return

    dwz_url = "http://sa.sogou.com/gettiny?={}"

    data = {"url": url}
    async with httpx.AsyncClient() as client:
        r: httpx.Response = await client.get(dwz_url, params=data)
        return r.text


def load_modules(path):
    """引入路径下所有包
    """
    for model in find_modules(path):
        try:
            import_string(model)
            logger.info(f'Load model: "{model}"')
        except Exception as e:
            logger.error(f'Failed to Load "{model}", error: {e}')
            logger.exception(e)
