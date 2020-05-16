import arrow
import feedparser
import httpx

from app.config import MyConfig


async def get_rss_info(url: str):
    async with httpx.AsyncClient(timeout=MyConfig.SUBSCIBE_INTERVAL) as client:
        response = await client.get(url)
        response.raise_for_status()
        return feedparser.parse(response.text or "")


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


def mk_msg_content(content, diffs: list):
    msg_list = []
    for item in diffs:
        msg = "【" + content.feed.title + "】有更新：\n----------------------\n"

        msg = msg + "标题：" + item["title"] + "\n"
        msg = msg + "链接：" + item["link"] + "\n"

        try:
            msg = (
                msg
                + "日期："
                + arrow.get(item["published_parsed"])
                .shift(hours=8)
                .format("YYYY-MM-DD HH:mm:ss")
            )
        except BaseException:
            msg = msg + "日期：" + arrow.now("Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss")
        msg_list.append(msg)
    return msg_list
