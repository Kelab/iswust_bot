"""
因为 `成绩` 部分爬取的教务处信息无法和课程表对应上，所以这里是独立的一个表，跟 course 表没有关系。
"""

from typing import Optional
from sqlalchemy import Column
from app.libs.gino import db
from .base import Base
from .user import User
from .course import Course
import pickle


class PlanScore(Base, db.Model):
    """计划课程成绩 Model
    """

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
    credit = Column(db.Float)
    score = Column(db.String(16))  # 可能考试成绩是 `通过`
    make_up_score = Column(db.String(16))  # 补考成绩
    gpa = Column(db.Float)
    season = Column(db.String(16))  # 春季 秋季 term中表现为春季2 秋季1

    @classmethod
    async def get_course_schedule(cls, qq) -> Optional[dict]:
        # 先查 user 出来，再查 Course 表
        user = await User.query.where(User.qq == qq).gino.first()
        # TODO 实现查表


class CreditProgress(Base, db.Model):
    """学分修读计划 Model
    """

    __tablename__ = "score_credit_progress"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    total = Column(db.Float)  # 总学分
    required = Column(db.Float)  # 必修课
    elective = Column(db.Float)  # 选修课
    sport = Column(db.Float)  # 体育类
    common = Column(db.Float)  # 全校通选
    degree = Column(db.Float)  # 学位课

    average_gpa = Column(db.Float)  # 平均绩点
    required_gpa = Column(db.Float)  # 必修课绩点
    degree_gpa = Column(db.Float)

    @classmethod
    async def get_all(cls, qq) -> Optional[dict]:
        # 先查 user 出来，再查 Course 表
        user = await User.get(qq)
        # TODO 实现查表
