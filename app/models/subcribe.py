from app.utils.rss import get_rss_info
from app.libs.gino import db
from .base import Base
from aiocqhttp import Event
from nonebot import context_id
import pickle
from loguru import logger
from datetime import datetime


class SubContent(Base, db.Model):
    """所有订阅内容 Model
    """

    __tablename__ = "sub_content"

    id_ = db.Column(
        "id", db.Integer, db.Sequence("sub_content_id_seq"), primary_key=True
    )
    intervel = db.Column(db.Integer)  # 更新速度，单位 s
    link = db.Column(db.String(128))
    name = db.Column(db.String(128))
    content = db.Column(db.LargeBinary)


class SubUser(Base, db.Model):
    """用户订阅 Model
    """

    __tablename__ = "sub_user"

    context_id = db.Column(db.String(64), primary_key=True)
    sub_id = db.Column(
        db.Integer,
        db.ForeignKey("sub_content.id", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    only_title = db.Column(db.Boolean, default=True)

    @staticmethod
    async def add_sub(
        event: Event, url: str, only_title=False, intervel=3000,
    ):
        # TODO: UTF8
        d = await get_rss_info(url)
        if not d:
            return None, None
        info = d["channel"]
        title = info.get("title", "无标题")
        items = info.get("items", [])
        logger.info(info)
        dumped_items = pickle.dumps(items)
        sub = await SubContent.create(
            intervel=intervel, link=url, name=title, content=dumped_items,
        )

        await SubUser.create(
            context_id=context_id(event), sub_id=sub.id_, only_title=only_title
        )
        return title, items
