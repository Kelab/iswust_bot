from app.libs.gino import db
from .base import Base
from sqlalchemy import Column


class SubContent(Base, db.Model):
    """所有订阅内容 Model
    """

    __tablename__ = "sub_content"

    id_ = Column("id", db.Integer, primary_key=True, autoincrement=True)
    intervel = Column(db.Integer)  # 更新速度，单位 s
    link = Column(db.LargeBinary)
    name = Column(db.String(64))
    last_update = Column(db.String(32))
    content = Column(db.LargeBinary)


class SubUser(Base, db.Model):
    """用户订阅 Model
    """

    __tablename__ = "sub_user"

    context_id = Column(db.Integer, primary_key=True)
    sub_id = Column(db.Integer, primary_key=True)
    only_title = Column(db.Boolean, default=True)
