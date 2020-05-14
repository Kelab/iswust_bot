"""
解析 学分修读进度
"""

from typing import List, TypedDict
from bs4 import BeautifulSoup

from app.constants.dean import API


class CreditProgressDict(TypedDict):
    total: float  # 总学分
    required: float  # 必修课
    elective: float  # 选修课
    sport: float  # 体育类
    common: float  # 全校通选
    degree: float  # 学位课
    average_gpa: float  # 平均绩点
    required_gpa: float  # 必修课绩点
    degree_gpa: float  # 学位课绩点


translator = {
    "总学分": "total",
    "必修课": "required",
    "选修课": "elective",
    "学位课": "degree",
    "全校通选": "common",
    "体育类": "sport",
    "平均绩点": "average_gpa",
    "必修课绩点": "required_gpa",
    "学位课绩点": "degree_gpa",
}


def get_credit_progress(sess) -> CreditProgressDict:
    """
    传入 requests 的 session
    返回 TypedDict：
    total: float  # 总学分
    required: float  # 必修课
    elective: float  # 选修课
    sport: float  # 体育类
    common: float  # 全校通选
    degree: float  # 学位课
    average_gpa: float  # 平均绩点
    required_gpa: float  # 必修课绩点
    degree_gpa: float  # 学位课绩点
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
    # 循环遍历每个 vlock 一共有上下两块
    for block in blocks:
        result[block.span.string] = block.em.text

    return result
