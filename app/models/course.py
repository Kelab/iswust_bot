import json
from typing import Union

from nonebot import get_bot
from nonebot.command import call_command
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from app.libs.aio import run_sync_func
from app.libs.gino import db
from app.libs.scheduler import add_job
from app.utils.bot import qq2event
from app.utils.parse.course_table import get_course_api

from .base import Base
from .user import User


class CourseStudent(Base, db.Model):
    """学生选课表 Model
    """

    __tablename__ = "course_student"

    student_id = Column(
        db.String(32),
        db.ForeignKey("user.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    course_json = Column(JSONB, nullable=False, server_default="{}")

    def __str__(self):
        return f"<CourseStudent id:{self.student_id}>"

    @classmethod
    async def add_or_update(cls, student_id, course_json) -> "CourseStudent":
        c_stu = await cls.get(student_id)
        if c_stu:
            await c_stu.update(course_json=course_json).apply()
        else:
            c_stu = await cls.create(student_id=student_id, course_json=course_json)
        return c_stu

    @classmethod
    async def get_course(cls, qq: int) -> Union["CourseStudent", str]:
        if not await User.check(qq):
            return "NOT_BIND"

        _bot = get_bot()
        query = cls.join(User).select()
        course_student = await query.where(User.qq == str(qq)).gino.first()
        if course_student is None:
            await add_job(cls.update_course, args=[qq])
            await _bot.send(qq2event(qq), "正在抓取课表，抓取过后我会直接发给你！")
            return "WAIT"
        return course_student

    @classmethod
    async def update_course(cls, qq: int):
        user: User = await User.get(str(qq))
        if not user:
            return
        sess = await User.get_session(user)
        res = await run_sync_func(get_course_api, sess)
        if res:
            c_stu = await cls.add_or_update(
                student_id=user.student_id, course_json=json.dumps(res)
            )
            await call_command(get_bot(), qq2event(qq), "cs")
            return c_stu
