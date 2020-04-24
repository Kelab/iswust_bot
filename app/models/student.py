from app.libs.gino import db
from .base import Base
from sqlalchemy import Column


class Student(Base, db.Model):
    __tablename__ = "student"

    student_id = Column(db.String(32), primary_key=True)
    password = Column(db.String(64), nullable=False)
    name = Column(db.String(64))
    sex = Column(db.String(16))
    birthday = Column(db.String(16))
    degree = Column(db.String(16))
    class_ = Column("class", db.String(16))
    major = Column(db.String(16))
    institute = Column(db.String(16))
    major_categories = Column(db.String(16))
    # TODO 移动到 redis 中
    cookies = Column(db.LargeBinary)
