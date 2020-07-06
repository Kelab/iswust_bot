from typing import TypedDict, List

import pandas as pd
import numpy as np
import regex as re
from bs4 import BeautifulSoup

from app.constants.dean import API

from .credit_progress import _parse_credit_progress, CreditProgressDict


def clear_lino1(table: pd.DataFrame):
    """这一步是把 columns 替换为第一行的内容
    并且 drop 掉第一行，重设 index
    """
    table.columns = table.iloc[0]
    table.drop(0, inplace=True)
    table.reset_index(inplace=True, drop=True)


def rm_nan(table: pd.DataFrame):
    """替换 NaN 为 无"""
    table.fillna("无", inplace=True)
    table.replace(np.nan, "无", regex=True, inplace=True)


def extract_term(df: pd.DataFrame):
    """解析出当前学期
    df 的第一行就是当前学期，使用正则表达式解析出相应的数据
    drop 掉第一行，并且重设 index
    """
    text = df.iloc[0][0]
    text = text.replace(" ", "")
    match = re.compile(r"(\d*-\d*)学年").match(text)
    if match:
        df.drop(0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return match.group(1)
    return None


def parse_score(sess):
    """传入 requests 的 session，这个函数负责请求页面
    然后爬取成绩页面 解析出来相应内容
    """

    res = sess.get(API.jwc_course_mark, verify=False)
    return _parse_score(res.text)


class ScoreDict(TypedDict):
    cet: pd.DataFrame
    plan: pd.DataFrame
    physical: pd.DataFrame
    common: pd.DataFrame
    summary: CreditProgressDict


def _parse_score(html) -> ScoreDict:
    """解析相应信息"""
    result: ScoreDict = {}  # type: ignore
    soup = BeautifulSoup(html, "lxml")
    b = soup.select_one("#contentArea > div.UIElement > ul > li > #welcome")
    result["cet"] = _parse_cet(b)
    result["plan"] = _parse_plan(b)  # 计划课程
    result["physical"] = _parse_physic_or_common(b, "physical")
    result["common"] = _parse_physic_or_common(b, "common")  # 通选课
    result["summary"] = _parse_credit_progress(html)
    return result


def _parse_cet(block):
    #  ["准考证号", "考试场次", "语言级别", "总分", "听力", "阅读", "写作", "综合"]
    table = pd.read_html(str(block.select("#CET table")))[0]
    clear_lino1(table)
    rm_nan(table)
    return table


def _parse_physic_or_common(block, cata: str) -> pd.DataFrame:
    # ["学期", "课程", "课程号", "学分", "正考", "补考", "绩点"]
    table = pd.read_html(str(block.select(f"#{cata.capitalize()} table")))[0]
    clear_lino1(table)
    rm_nan(table)
    # 最后一行是学分绩点计算
    table.drop(len(table) - 1, inplace=True)
    return table


def _parse_plan(block) -> pd.DataFrame:
    _tables = pd.read_html(str(block.select("#Plan table")))
    df_lst = []  # type: List[pd.DataFrame]
    for table in _tables:
        table.dropna(thresh=len(table.columns) - 2, inplace=True)  # 去除 NaN 行
        table.reset_index(drop=True, inplace=True)
        # line 0: 哪个学期
        term = extract_term(table)
        if not term:
            continue
        start_index = 0
        for idx, series in table.iterrows():
            text = series[0]
            # 找到 `平均学分绩点` 这一行进行切分，分为上下两部分
            if text.startswith("平均学分绩点"):
                new_df = table.iloc[start_index:idx].copy()
                new_df.reset_index(inplace=True, drop=True)
                clear_lino1(new_df)
                rm_nan(new_df)
                # 学期名 春/秋
                # 替换 春/秋 为 season
                new_df.rename(columns={new_df.iat[0, 0]: "season"}, inplace=True)
                new_df["term"] = [term] * len(new_df.index)
                start_index = idx + 1
                df_lst.append(new_df)
    result = pd.concat(df_lst, ignore_index=True)
    return result
