"""
因为 `成绩` 部分爬取的教务处信息无法和课程表对应上，所以这里是独立的一个表，跟 course 表没有关系。
"""
from collections import defaultdict
from typing import List

import pandas as pd
from aiocqhttp import Event
from nonebot import get_bot
from sqlalchemy import Column

from app.libs.gino import db
from app.models.user import User
from app.utils.parse.score import ScoreDict
from app.bot.score.utils import tabulate
from .base import Base


class PlanScore(Base, db.Model):
    """计划课程成绩 Model
    """

    _cn_list = ["课程", "课程号", "学分", "课程性质", "正考", "补考", "绩点"]
    _en_list = [
        "course_name",
        "course_id",
        "credit",
        "property_",
        "score",
        "make_up_score",
        "gpa",
    ]
    __tablename__ = "score_plan"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    course_id = Column(db.String(16), primary_key=True)
    term = Column(db.String(64), primary_key=True)  # 学期
    course_name = Column(db.String(64))
    property_ = Column("property", db.String(64))  # 必修 选修 限选
    credit = Column(db.String(16))
    score = Column(db.String(16))  # 可能考试成绩是 `通过`
    make_up_score = Column(db.String(16))  # 补考成绩
    gpa = Column(db.String(16))
    season = Column(db.String(16))  # 春季 秋季 term中表现为春季2 秋季1

    @classmethod
    async def add_or_update_one(cls, student_id, term, season, series):
        kwargs = dict(student_id=student_id, term=term, season=season)
        for cn_key, en_key in zip(cls._cn_list, cls._en_list):
            kwargs[en_key] = series[cn_key]
        sco = (
            await cls.query.where(cls.student_id == student_id)
            .where(cls.course_id == series["课程号"])
            .where(cls.term == term)
            .gino.first()
        )
        if sco:
            await sco.update(**kwargs).apply()
        else:
            await cls.create(**kwargs)

    @classmethod
    async def add_or_update(cls, student_id, plan):
        terms = pd.unique(plan["term"])
        for term in terms:
            _term = plan[plan["term"] == term]
            seasons = pd.unique(_term["season"])
            for season in seasons:
                data = _term[_term["season"] == season]
                for _, series in data.iterrows():
                    await cls.add_or_update_one(student_id, term, season, series)

    @classmethod
    def to_df(cls, plan_scores: List["PlanScore"]):
        dct = defaultdict(list)
        for item in plan_scores:
            for en, cn in zip(PlanScore._en_list, PlanScore._cn_list):
                dct[cn].append(getattr(item, en, None))
            dct["term"].append(getattr(item, "term", None))
            dct["season"].append(getattr(item, "season", None))

        df = pd.DataFrame(data=dct)
        return df

    @classmethod
    async def check_update(cls, event: Event, plan: pd.DataFrame):
        old_score = await cls.load_score(event)
        if old_score is None:
            return
        diffs = diff(plan, old_score)
        if not diffs.empty:
            bot = get_bot()
            await bot.send(event, f"有新的成绩：\n{tabulate(diffs)}")

    @classmethod
    async def load_score(cls, event: Event) -> pd.DataFrame:
        user = await User.check(event.user_id)
        if not user:
            return
        scores = await cls.query.where(cls.student_id == user.student_id).gino.all()
        if not scores:
            return
        df = cls.to_df(scores)
        return df


class PhysicalOrCommonScore(Base, db.Model):
    """计划课程成绩 Model
    """

    _cn_list = ["学期", "课程", "课程号", "学分", "正考", "补考", "绩点"]
    _en_list = [
        "term",
        "course_name",
        "course_id",
        "credit",
        "score",
        "make_up_score",
        "gpa",
    ]
    __tablename__ = "score_physic_or_common"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    course_id = Column(db.String(16), primary_key=True)
    term = Column(db.String(64), primary_key=True)  # 学期
    course_name = Column(db.String(64))
    credit = Column(db.String(16))
    score = Column(db.String(16))  # 可能考试成绩是 `通过`
    make_up_score = Column(db.String(16))  # 补考成绩
    gpa = Column(db.String(16))
    cata = Column(db.String(16))  # common 或 physical

    @classmethod
    async def add_or_update_one(cls, student_id, cata, series):
        kwargs = dict(student_id=student_id, cata=cata)
        for cn_key, en_key in zip(cls._cn_list, cls._en_list):
            kwargs[en_key] = series[cn_key]
        sco = (
            await cls.query.where(cls.student_id == student_id)
            .where(cls.course_id == series["课程号"])
            .where(cls.term == series["学期"])
            .gino.first()
        )
        if sco:
            await sco.update(**kwargs).apply()
        else:
            await cls.create(**kwargs)

    @classmethod
    async def add_or_update(cls, student_id, score_dict, cata):
        table = score_dict[cata]
        for _, series in table.iterrows():
            await cls.add_or_update_one(student_id, cata, series)


class CETScore(Base, db.Model):
    """计划课程成绩 Model
    """

    _cn_list = ["准考证号", "考试场次", "语言级别", "总分", "听力", "阅读", "写作", "综合"]
    _en_list = [
        "exam_id",
        "exam_name",
        "level",
        "total",
        "listen",
        "read",
        "write",
        "common",
    ]
    __tablename__ = "score_cet"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )

    exam_id = Column(db.String(32), primary_key=True)
    exam_name = Column(db.String(64))
    level = Column(db.String(16))
    total = Column(db.String(16))
    listen = Column(db.String(16))
    read = Column(db.String(16))
    write = Column(db.String(16))
    common = Column(db.String(16))

    @classmethod
    async def add_or_update_one(cls, student_id, series):
        kwargs = dict(student_id=student_id)
        for cn_key, en_key in zip(cls._cn_list, cls._en_list):
            kwargs[en_key] = series[cn_key]
        sco = (
            await cls.query.where(cls.student_id == student_id)
            .where(cls.exam_id == series["准考证号"])
            .gino.first()
        )
        if sco:
            await sco.update(**kwargs).apply()
        else:
            await cls.create(**kwargs)

    @classmethod
    async def add_or_update(cls, student_id, table):
        for _, series in table.iterrows():
            await cls.add_or_update_one(student_id, series)


async def save_score(user, score: ScoreDict):
    await CETScore.add_or_update(user.student_id, score["cet"])
    await PhysicalOrCommonScore.add_or_update(user.student_id, score, "common")
    await PhysicalOrCommonScore.add_or_update(user.student_id, score, "physical")
    await PlanScore.add_or_update(user.student_id, score["plan"])


def diff(new, old) -> pd.DataFrame:
    result = []
    for idx, n_series in new.iterrows():
        flag = 0
        for _, o_series in old.iterrows():
            if (
                n_series["课程号"] == o_series["课程号"]
                and n_series["term"] == o_series["term"]
                and n_series["season"] == o_series["season"]
            ):
                flag = 1
                break
        if flag == 0:
            result.append(idx)
    df = new.iloc[result]
    return df
