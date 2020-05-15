"""
解析 学分修读进度
"""

from typing import List, TypedDict
from bs4 import BeautifulSoup

from app.constants.dean import API


class CreditProgressDict(TypedDict):
    总学分: float
    必修课: float
    选修课: float
    体育类: float
    全校通选: float
    学位课: float
    平均绩点: float
    必修课绩点: float
    学位课绩点: float


def get_credit_progress(sess) -> CreditProgressDict:
    """传入 requests 的 session
    """

    res = sess.get(API.jwc_course_mark, verify=False)
    json = _parse_credit_progress(res.text)

    return json


def _parse_credit_progress(html) -> CreditProgressDict:
    """
    :param html: 网页
    :return: dict
    """
    result: CreditProgressDict = {}  # type: ignore
    soup: BeautifulSoup = BeautifulSoup(html, "lxml")
    blocks: List[BeautifulSoup] = soup.select("div.UICircle > ul.boxNavigation > li")
    # 循环遍历每个 block 一共有上下两块
    for block in blocks:
        result[block.span.string] = block.em.text

    return result
