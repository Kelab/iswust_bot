import pandas as pd

from app.bot.credit.service import _format as _format_credit
from app.utils.bot import qq2event, send_msgs
from app.utils.parse.score import ScoreDict


def calc_gpa(table, jidian_col="绩点", xuefen_col="学分", required=False):
    table[jidian_col] = pd.to_numeric(table[jidian_col])
    table[xuefen_col] = pd.to_numeric(table[xuefen_col])
    result = {"mean": round(table[jidian_col].sum() / table[xuefen_col].sum(), 3)}
    if required:
        _required = table[table["课程性质"] == "必修"]
        result["required"] = round(
            _required[jidian_col].sum() / _required[xuefen_col].sum(), 3,
        )
    return result


async def send_score(user, score: ScoreDict):
    msgs = []
    msgs.append(_format_cet(score["cet"]))
    msgs.append(_format_physical_or_physical(score, "common"))
    msgs.append(_format_physical_or_physical(score, "physical"))
    msgs.extend(_format_plan(score["plan"]))
    msgs.append(_format_credit(score["summary"]))
    await send_msgs(qq2event(user.qq), msgs)


def _format_cet(table):
    msg = "四六级成绩：\n---------\n"
    for _, series in table.iterrows():
        msg += str(series["考试场次"]) + "\n"
        msg += "- 准考证号：" + str(series["准考证号"]) + "\n"
        msg += "- 语言级别：" + str(series["语言级别"])
        msg += "   总分：" + str(series["总分"]) + "\n"
        msg += "- 听力：" + str(series["听力"])
        msg += "   阅读：" + str(series["阅读"]) + "\n"
        msg += "- 写作：" + str(series["写作"])
        msg += "   综合：" + str(series["综合"]) + "\n"
    return msg


def _format_physical_or_physical(score, cata):
    cata_cn = "体育成绩" if cata == "physical" else "全校通选课"
    df = score[cata]
    return (
        f"{cata_cn}：\n"
        + tabulate(df, is_common_physic=True)
        + f"平均绩点：{calc_gpa(df)['mean']}\n"
    )


def _format_plan(plan):
    term_score = []
    terms = pd.unique(plan["term"])
    for term in terms:
        _term = plan[plan["term"] == term]
        seasons = pd.unique(_term["season"])
        for season in seasons:
            data = _term[_term["season"] == season]
            jidian = calc_gpa(data, required=True)
            term_score.append(
                f"{term} {season}\n"
                + tabulate(data)
                + f"\n平均绩点：{jidian['mean']}\n"
                + f"必修绩点：{jidian['required']}\n"
            )
    term_score.reverse()
    return term_score


def tabulate(table, is_common_physic=False):
    msg = "---------\n"
    for _, series in table.iterrows():
        if is_common_physic:
            msg += str(series["学期"]) + "\n"
        if not is_common_physic:
            msg += "[" + str(series["课程性质"]) + "] "
        msg += str(series["课程"]) + "\n"
        msg += "- 学分：" + str(series["学分"])
        msg += "   绩点：" + str(series["绩点"]) + "\n"
        msg += "- 正考：" + str(series["正考"])
        msg += "   补考：" + str(series["补考"]) + "\n"

    return msg
