import httpx
import feedparser


async def get_rss_info(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return feedparser.parse(response.text)


def check_update(new, old) -> list:
    a = new.entries
    b = old["entries"]
    c = []

    for i in a:
        count = 0
        for j in b:
            if i["link"] == j["link"]:
                count = 1
        if count == 0:
            c.append(i)
    return c
