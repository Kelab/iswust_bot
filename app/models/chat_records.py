from app.libs.gino import db
from .base import Base
from sqlalchemy import Column
from aiocqhttp import Event
from nonebot import context_id


class ChatRecords(Base, db.Model):
    __tablename__ = "chat_records"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    self_id = Column(db.Integer)
    ctx_id = Column(db.String(64))
    msg = Column(db.String)

    @classmethod
    async def add_msg(cls, event: Event):
        await ChatRecords.create(
            self_id=event.self_id, ctx_id=context_id(event), msg=str(event.message)
        ),
