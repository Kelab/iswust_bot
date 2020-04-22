from app.libs.gino import db
from .base import Base


class Grade(Base, db.Model):
    __tablename__ = "grade"

    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    gname = db.Column(db.String(64))
    gterm = db.Column(db.String(64))
    course_number = db.Column(db.String(64))
    credit = db.Column(db.Integer)
    xingzhi = db.Column(db.String(64))
    zhengkao = db.Column(db.Integer)
    bukao = db.Column(db.Integer)
    jidian = db.Column(db.Integer)
