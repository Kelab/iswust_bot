import pickle

from app.libs.gino import db
from .base import Base


class Course(Base, db.Model):
    __tablename__ = "course"

    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    course_table = db.Column(db.BLOB)

    @classmethod
    async def get_course_schedule(cls, qq) -> dict:
        cour = Course.query.filter_by(qq=qq).first()
        if cour is not None:
            return pickle.loads(cour.course_table)
