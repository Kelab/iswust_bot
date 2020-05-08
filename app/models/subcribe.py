import pickle

from aiocqhttp import Event
from loguru import logger
from nonebot import context_id, get_bot
from nonebot.helpers import send

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

    def __repr__(self):
        return f"<SubUser {self.ctx_id} {self.link}>"

    @classmethod
    async def add_sub(cls, event: Event, url: str, only_title=False):
        # TODO: UTF8
        try:
            d = await get_rss_info(url)
        except Exception:
            await send(get_bot(), event, "获取订阅信息失败，但已添加到订阅中，我们会稍后重试。")
            d = {"channel": {}}

        if not d:
            return None
        info = d["channel"]
        title = info.get("title", "无标题")
        logger.info(info)
        sub = await SubContent.add_or_update(
            link=url, name=title, content=pickle.dumps(d),
        )
        await SubUser.create(
            ctx_id=context_id(event, mode="group"), link=sub.link, only_title=only_title
        )
        return title

    @classmethod
    async def get_sub(cls, event: Event, url: str):
        ctx_id = context_id(event, mode="group")
        loader = SubUser.load(sub_content=SubContent)
        sub = (
            await cls.outerjoin(SubContent)
            .select()
            .where(cls.link == url)
            .where(cls.ctx_id == ctx_id)
            .gino.load(loader)
            .first()
        )
        return sub

    @classmethod
    async def get_user_subs(cls, event: Event):
        ctx_id = context_id(event, mode="group")
        loader = SubUser.load(sub_content=SubContent)
        sub = (
            await cls.outerjoin(SubContent)
            .select()
            .where(cls.ctx_id == ctx_id)
            .gino.load(loader)
            .all()
        )
        return sub

    @classmethod
    async def remove_sub(cls, event: Event, url: str):
        ctx_id = context_id(event, mode="group")
        sub = (
            await cls.query.where(cls.link == url)
            .where(cls.ctx_id == ctx_id)
            .gino.first()
        )
        await sub.delete()
        return True

    @classmethod
    async def get_user(cls, url: str):
        sub = await cls.query.where(cls.link == url).gino.all()
        return sub
