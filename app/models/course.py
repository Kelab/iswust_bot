from sqlalchemy import Column
from app.libs.gino import db
from app.utils.bot_common import qq2event

from .base import Base
from .user import User

from loguru import logger
from nonebot import get_bot


class Course(Base, db.Model):
    """课程表 Model
    """

    __tablename__ = "course"

    id_ = Column("id", db.Integer, db.Sequence("course_id_seq"), primary_key=True)
    term = Column(db.String(32))  # 学期
    course_name = Column(db.String(64))
    course_idx = Column(db.String(16))  # 课程序号 001 002 那些
    time4class = Column(db.String(64))  # 上课时间
    teacher_name = Column(db.String(32))  # 上课教师
    location = Column(db.String(64))
    course_table = Column(db.LargeBinary)
    start_week = Column(db.Integer)
    end_week = Column(db.Integer)

    def __str__(self):
        return f"<Course id:{self.id_} course_name:{self.course_name}>"


class CourseStudent(Base, db.Model):
    """学生选课表 Model
    """

    __tablename__ = "course_student"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    course_id = Column(
        db.Integer,
        db.ForeignKey("course.id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )

    @classmethod
    async def get_course(cls, qq: str):
        _bot = get_bot()

        query = cls.join(User).select()
        loader = cls.load(course=Course.on(cls.course_id == Course.id_))
        course_student = await query.where(User.qq == str(qq)).gino.load(loader).first()
        if course_student is None:
            await _bot.send(qq2event(qq), "正在抓取课表，抓取过后我会直接发给你！")
        else:
            logger.info(course_student.course)
        return {}

    @classmethod
    async def update_course(cls, qq: str):
        _bot = get_bot()

        query = cls.join(User).select()
        loader = cls.load(course=Course.on(cls.course_id == Course.id_))
        course_student = await query.where(User.qq == str(qq)).gino.load(loader).first()
        if course_student is None:
            await _bot.send(qq2event(qq), "正在抓取课表，抓取过后我会直接发给你！")
        else:
            logger.info(course_student.course)
        return {}
