from typing import TypedDict, List, Dict

import pandas as pd
import regex as re
from bs4 import BeautifulSoup

from app.constants.dean import API

from .credit_progress import _parse_credit_progress, CreditProgressDict


def extract_df(dom) -> pd.DataFrame:
    _table = pd.read_html(str(dom.select("table")))
    table = _table[0]
    return table


def clear_lino1(table: pd.DataFrame):
    table.columns = table.iloc[0]
    table.drop(0, inplace=True)
    table.reset_index(inplace=True, drop=True)


def rm_nan(table: pd.DataFrame):
    table.fillna("无", inplace=True)
    table.replace(pd.np.nan, "无", regex=True, inplace=True)


_p = re.compile(r"(\d*-\d*)学年")


def extract_term(df: pd.DataFrame):
    text = df.iloc[0][0]
    text = text.replace(" ", "")
    match = _p.match(text)
    if match:
        df.drop(0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return match.group(1)
    return None


def get_score(sess):
    """传入 requests 的 session
    """

    res = sess.get(API.jwc_course_mark, verify=False)
    return _parse_score(res.text)


class TermDict(TypedDict):
    data: pd.DataFrame  # `春/秋` 季学期数据
    season: str


class ScoreDict(TypedDict):
    cet: pd.DataFrame
    plan: Dict[str, List[TermDict]]
    physical: pd.DataFrame
    common: pd.DataFrame
    summary: CreditProgressDict


def _parse_score(html) -> ScoreDict:
    summary_dict = _parse_credit_progress(html)
    result: ScoreDict = {}  # type: ignore
    soup = BeautifulSoup(html, "lxml")
    all_ = soup.select_one("#contentArea > div.UIElement > ul > li > #welcome")
    plan = all_.select_one("#Plan")  # 计划课程
    common = all_.select_one("#Common")  # 通选课
    physical = all_.select_one("#Physical")
    cet = all_.select_one("#CET")
    result["cet"] = _parse_cet(cet)
    result["plan"] = _parse_plan(plan)
    result["physical"] = _parse_physic_or_common(physical)
    result["common"] = _parse_physic_or_common(common)
    result["summary"] = summary_dict
    return result


def _parse_cet(dom):
    table = extract_df(dom)
    #  ["准考证号", "考试场次", "语言级别", "总分", "听力", "阅读", "写作", "综合"]
    clear_lino1(table)
    rm_nan(table)
    return table


def _parse_physic_or_common(dom) -> pd.DataFrame:
    table = extract_df(dom)
    # ["学期", "课程", "课程号", "学分", "正考", "补考", "绩点"]
    clear_lino1(table)
    rm_nan(table)
    # 最后一行是学分绩点计算
    table.drop(len(table) - 1, inplace=True)
    return table


def _parse_plan(dom) -> Dict[str, List[TermDict]]:
    _tables = pd.read_html(str(dom.select("table")))
    result = {}
    for table in _tables:
        table.dropna(thresh=len(table.columns) - 2, inplace=True)  # 去除 NaN 行
        table.reset_index(drop=True, inplace=True)
        # line 0: 哪个学期
        term = extract_term(table)
        if not term:
            continue
        term_lst = []  # type: List[TermDict]
        start_index = 0
        for idx, series in table.iterrows():
            term_dct: TermDict = {}  # type: ignore
            text = series[0]
            # 找到 `平均学分绩点` 这一行进行切分，分为上下两部分
            if text.startswith("平均学分绩点"):
                new_df = table.iloc[start_index:idx].copy()
                new_df.reset_index(inplace=True, drop=True)
                # 学期名 春 秋
                term_dct["season"] = new_df.iat[0, 0]
                # drop 掉 season 这一列
                clear_lino1(new_df)
                rm_nan(new_df)
                term_dct["data"] = new_df
                start_index = idx + 1
                term_lst.append(term_dct)
        result[term] = term_lst
    return result
