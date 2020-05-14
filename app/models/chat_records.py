from app.libs.gino import db
from .base import Base
from sqlalchemy import Column
from aiocqhttp import Event
from nonebot import context_id


class ChatRecords(Base, db.Model):
    """保存聊天记录 Model
    """

    __tablename__ = "chat_records"

    id_ = Column("id", db.Integer, db.Sequence("chat_records_id_seq"), primary_key=True)
    self_id = Column(db.String(32))
    ctx_id = Column(db.String(64))
    msg = Column(db.String)
    out = Column(db.Boolean, default=False)

    @classmethod
    async def add_msg(cls, event: Event, out: bool = False):
        await ChatRecords.create(
            self_id=str(event.self_id),
            ctx_id=context_id(event),
            msg=str(event.message),
            out=out,
        ),
