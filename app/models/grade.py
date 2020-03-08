from . import db


class Grade(db.Model):
    __tablename__ = "grade"

    gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    grade = db.Column(db.TEXT)
