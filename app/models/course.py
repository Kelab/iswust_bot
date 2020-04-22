import pickle
from typing import Optional

from app.libs.gino import db
from .base import Base


class Course(Base, db.Model):
    __tablename__ = "course"

    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_table = db.Column(db.BLOB)
    cname = db.Column(db.String(64))
    clocation = db.Column(db.String(64))
    ctime = db.Column(db.String(64))
    cstart = db.Column(db.Integer)
    cend = db.Column(db.Integer)

    @classmethod
    async def get_course_schedule(cls, qq) -> Optional[dict]:
        cour = Course.query.filter_by(qq=qq).first()
        if cour is not None:
            return pickle.loads(cour.course_table)
