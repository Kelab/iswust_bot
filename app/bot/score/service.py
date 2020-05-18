from typing import Optional

import pandas as pd
from loguru import logger
from nonebot import get_bot

from app.bot.credit.service import _format as _format_credit
from app.libs.aio import run_sync_func
from app.libs.cache import cache
from app.libs.scheduler import add_job
from app.models.user import User
from app.models.score import save_score, PlanScore
from app.utils.bot import qq2event, send_msgs
from app.utils.parse.score import ScoreDict, parse_score


class ScoreService:
    @classmethod
    async def get_score(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._get, args=[user])
        _bot = get_bot()
        await _bot.send(qq2event(qq), "正在抓取成绩，抓取过后我会直接发给你！")
        return "WAIT"

    @classmethod
    async def _get(cls, user: User):
        try:
            key = f"score/{user.qq}"
            res = await cache.get(key)
            if not res:
                sess = await User.get_session(user)
                res: ScoreDict = await run_sync_func(parse_score, sess)
                if res:
                    await cache.set(key, res, ttl=600)
                else:
                    raise ValueError("查询成绩出错")
            await save_score(user.student_id, res)
            msgs = await get_msgs(res)
            await send_msgs(qq2event(user.qq), msgs)
        except Exception as e:
            logger.exception(e)
            _bot = get_bot()
            await _bot.send(qq2event(user.qq), "查询成绩出错，请稍后再试")

    @classmethod
    async def load_score(cls, qq: int) -> Optional[str]:
        # 先查 user 出来，再查 Course 表
        user = await User.check(qq)
        if not user:
            return "NOT_BIND"
        await add_job(cls._load_score, args=[user])
        _bot = get_bot()
        await _bot.send(qq2event(qq), "正在load成绩")
        return "WAIT"

    @classmethod
    async def _load_score(cls, user: User) -> Optional[str]:

        # 先查 user 出来，再查 Course 表
        scores = await PlanScore.query.where(
            PlanScore.student_id == user.student_id
        ).gino.all()
        if not scores:
            return
        df = PlanScore.to_df(scores)
        _bot = get_bot()
        await _bot.send(qq2event(user.qq), str(df))


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


async def get_msgs(score: ScoreDict):
    msgs = []
    msgs.append(_format_cet(score["cet"]))
    msgs.append(_format_physical_or_physical(score, "common"))
    msgs.append(_format_physical_or_physical(score, "physical"))
    msgs.extend(_format_plan(score["plan"]))
    msgs.append(_format_credit(score["summary"]))
    return msgs


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
