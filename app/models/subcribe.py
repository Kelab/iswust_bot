from app.utils.rss import get_rss_info
from app.libs.gino import db
from .base import Base
from sqlalchemy import Column
from aiocqhttp import Event
from nonebot import context_id
import pickle
from loguru import logger


class SubContent(Base, db.Model):
    """所有订阅内容 Model
    """

    __tablename__ = "sub_content"

    id_ = Column("id", db.Integer, primary_key=True, autoincrement=True)
    intervel = Column(db.Integer)  # 更新速度，单位 s
    link = Column(db.String(128))
    name = Column(db.String(64))
    last_update = Column(db.String(32))
    content = Column(db.LargeBinary)


class SubUser(Base, db.Model):
    """用户订阅 Model
    """

    __tablename__ = "sub_user"

    context_id = Column(db.Integer, primary_key=True)
    sub_id = Column(
        db.Integer,
        db.ForeignKey("sub_content.id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    only_title = Column(db.Boolean, default=True)

    @staticmethod
    async def add_sub(
        event: Event, url: str, only_title=False, intervel=3000,
    ):
        d = await get_rss_info(url)
        if not d:
            return None, None
        info = d["channel"]
        title = info.get("title", "无标题")
        items = info.get("items", [])
        logger.info(info)
        items = pickle.dumps(items)
        sub = await SubContent.create(
            intervel=intervel, link=url, name=title, content=items, last_update="123",
        )

        await SubUser.create(
            context_id=context_id(event), sub_id=sub.id, only_title=only_title
        )
        return title, items
