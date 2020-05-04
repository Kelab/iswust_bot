import httpx
from httpx.config import Timeout
import feedparser


async def get_rss_info(url: str):
    async with httpx.AsyncClient(timeout=Timeout(30)) as client:
        response = await client.get(url)
        return feedparser.parse(response.text)


def diff(new, old) -> list:
    new_items = new.entries
    old_items = old.entries
    result = []

    for new in new_items:
        flag = 0
        for old in old_items:
            if new["link"] == old["link"]:
                flag = 1
                break
        if flag == 0:
            result.append(new)
    return result
