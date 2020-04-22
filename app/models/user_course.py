from app.libs.gino import db
from .base import Base


class UserCourse(Base, db.Model):
    __tablename__ = "user_course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.String(16), db.ForeignKey("course.id"))
    term = db.Column(db.String(64))  # 学期
    property = db.Column(db.String(64))  # 必修 选修 限选
    credit = db.Column(db.Float)
    score = db.Column(db.Float)
    make_up_score = db.Column(db.Float)  # 补考成绩
    gpa = db.Column(db.Float)
