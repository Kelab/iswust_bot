import pickle

from aiocqhttp import Event
from loguru import logger
from nonebot import context_id

from app.libs.gino import db
from app.utils.rss import get_rss_info

from .base import Base


class SubContent(Base, db.Model):
    """所有订阅内容 Model
    """

    __tablename__ = "sub_content"

    link = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128))
    content = db.Column(db.LargeBinary)

    @classmethod
    async def add_or_update(cls, link, name, content) -> "SubContent":
        sub = await cls.get(link)
        if sub:
            await sub.update(link=link, name=name, content=content).apply()
        else:
            sub = await cls.create(link=link, name=name, content=content)
        return sub


class SubUser(Base, db.Model):
    """用户订阅 Model
    """

    __tablename__ = "sub_user"

    ctx_id = db.Column(db.String(64), primary_key=True)
    link = db.Column(
        db.String(128),
        db.ForeignKey("sub_content.link", onupdate="CASCADE", ondelete="SET NULL"),
        primary_key=True,
    )
    only_title = db.Column(db.Boolean, default=True)

    @classmethod
    async def add_sub(cls, event: Event, url: str, only_title=False):
        # TODO: UTF8
        d = await get_rss_info(url)
        if not d:
            return None, None
        info = d["channel"]
        title = info.get("title", "无标题")
        items = info.get("items", [])
        logger.info(info)
        sub = await SubContent.add_or_update(
            link=url, name=title, content=pickle.dumps(d),
        )
        await SubUser.create(
            ctx_id=context_id(event), link=sub.link, only_title=only_title
        )
        return title, items

    @classmethod
    async def get_sub(cls, event: Event, url: str):
        ctx_id = context_id(event)
        sub = (
            await cls.query.where(cls.link == url)
            .where(cls.ctx_id == ctx_id)
            .gino.first()
        )
        return sub
