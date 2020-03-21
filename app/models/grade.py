from app.libs.gino import db
from .base import Base


class Grade(Base, db.Model):
    __tablename__ = "grade"

    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    grade = db.Column(db.TEXT)
