from typing import List
from app.env import env

rsshub_url: str = env("RSSHUB_URL", "")
rsshub_url = rsshub_url.rstrip("/")

rss_info = {
    "教务处新闻": "/swust/jwc/news",
    "教务处通知 创新创业教育": "/swust/jwc/notice/1",
    "教务处通知 学生学业": "/swust/jwc/notice/2",
    "教务处通知 建设与改革": "/swust/jwc/notice/3",
    "教务处通知 教学质量保障": "/swust/jwc/notice/4",
    "教务处通知 教学运行": "/swust/jwc/notice/5",
    "教务处通知 教师教学": "/swust/jwc/notice/6",
    "计科学院通知 新闻动态": "/swust/cs/1",
    "计科学院通知 学术动态": "/swust/cs/2",
    "计科学院通知 通知公告": "/swust/cs/3",
    "计科学院通知 教研动态": "/swust/cs/4",
}


def get_rss_list():
    msg = "0. 所有\n"
    for idx, key in enumerate(rss_info.keys()):
        msg = msg + f"{idx+1}. {key}\n"

    return msg


def make_url(idx: int) -> List[str]:
    if 0 >= idx >= len(rss_info):
        return []
    if idx == 0:
        url = [rsshub_url + u for u in list(rss_info.values())]
    else:
        _url = rss_info[list(rss_info.keys())[idx]]
        url = [rsshub_url + _url]
    return url
