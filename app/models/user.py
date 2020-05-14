import json
import pickle

from loguru import logger
from nonebot import get_bot
from sqlalchemy import Column

from app.constants.dean import API
from app.libs.aio import run_sync_func
from app.libs.gino import db
from app.utils.bot_common import qq2event

from .base import Base


class User(Base, db.Model):
    """用户表 Model
    """

    __tablename__ = "user"

    qq = Column(db.String(16), primary_key=True)
    student_id = Column(db.String(32), unique=True)
    password = Column(db.String(64), nullable=False)
    name = Column(db.String(64))
    class_ = Column("class", db.String(16))
    cookies = Column(db.LargeBinary)

    @classmethod
    async def add(
        cls, *, qq: int, student_id: int, password: str, user_info: dict, cookies
    ):
        body = user_info.get("body", {})
        result = body.get("result", "{}")
        result = json.loads(result)
        user = User(
            student_id=str(student_id),
            qq=str(qq),
            password=password,
            cookies=cookies,
            class_=result.get("class"),
            name=result.get("name"),
        )
        await user.create()
        return user

    @classmethod
    async def unbind(cls, qq: int):
        user = await User.query.where(User.qq == str(qq)).gino.first()
        await user.delete()
        return True

    @classmethod
    async def check(cls, qq: int):
        user = await cls.get(str(qq))
        if user:
            return user
        _bot = get_bot()
        await _bot.send(qq2event(qq), "未绑定，试试对我发送 `绑定`")
        return False

    @classmethod
    async def get_cookies(cls, qq: int):
        user = await cls.get(str(qq))
        if not user:
            return False
        from auth_swust import Login
        from auth_swust import request as login_request

        cookies = pickle.loads(user.cookies)
        sess = login_request.Session(cookies)
        res = await run_sync_func(
            sess.get, API.jwc_index, allow_redirects=False, verify=False
        )

        # 302重定向了，session失效，刷新
        if res.status_code == 302 or res.status_code == 301:
            logger.info("qq {} 的session 失效".format(qq))

            u_ = Login(user.student_id, user.password)
            is_log, _ = await run_sync_func(u_.try_login)
            if is_log:
                cookies = pickle.dumps(u_.get_cookies())
                await user.update(cookies=cookies).apply()
                return u_.get_cookies()
        else:
            return cookies
