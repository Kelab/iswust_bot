from sqlalchemy import Column
from app.libs.gino import db
from .base import Base


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


class CourseStudent(Base, db.Model):
    """学生选课表 Model
    """

    __tablename__ = "course_student"

    student_id = Column(
        db.String(32),
        db.ForeignKey("student.student_id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    course_id = Column(
        db.Integer,
        db.ForeignKey("course.id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
