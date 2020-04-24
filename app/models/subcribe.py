from app.libs.gino import db
from .base import Base
from sqlalchemy import Column


class SubContent(Base, db.Model):
    __tablename__ = "sub_content"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    intervel = Column(db.Integer)  # 更新速度，单位 s
    link = Column(db.LargeBinary)
    name = Column(db.String(64))
    last_update = Column(db.String(32))
    content = Column(db.LargeBinary)


class UserSub(Base, db.Model):
    __tablename__ = "user_sub"

    user_id = Column(db.Integer)
    sub_id = Column(db.Integer)
    group_id = Column(db.Integer)
    only_title = Column(db.Boolean, default=True)
