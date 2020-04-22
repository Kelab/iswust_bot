import pickle
from typing import Optional

from app.libs.gino import db
from .base import Base


class Course(Base, db.Model):
    __tablename__ = "course"

    id = db.Column(db.String(16), primary_key=True)
    course_table = db.Column(db.LargeBinary)
    name = db.Column(db.String(64))
    teacher_name = db.Column(db.String(32))
    location = db.Column(db.String(64))
    class_time = db.Column(db.String(64))
    start_week = db.Column(db.Integer)
    end_week = db.Column(db.Integer)

    @classmethod
    async def get_course_schedule(cls, qq) -> Optional[dict]:
        cour = Course.query.filter_by(qq=qq).first()
        if cour is not None:
            return pickle.loads(cour.course_table)
