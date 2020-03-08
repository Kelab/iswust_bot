from . import db


class Course(db.Model):
    __tablename__ = "course"

    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    course_table = db.Column(db.BLOB)
