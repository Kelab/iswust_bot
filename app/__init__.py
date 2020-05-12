from os import path
from typing import Any
from loguru import logger

import nonebot as nb
from nonebot import NoneBot, default_config
from quart import Quart

from .libs.gino import init_db
from .libs.cache import init_cache
from .libs.scheduler import init_scheduler
from .libs.roconfig import Configuration

from .utils.tools import load_modules


def init_bot(config_object: Any) -> nb.NoneBot:
    nb.init(config_object)
    bot = nb.get_bot()

    nb.load_builtin_plugins()
    nb.load_plugins(path.join(path.dirname(__file__), "bot"), "app.bot")

    return bot


def load_config():
    from .config import MyConfig

    conf = Configuration()
    conf.add_object(default_config)
    conf.add_object(MyConfig)
    logger.info(conf.to_dict())
    return conf.to_config()


def register_blueprint(app: Quart):
    load_modules("app.api")
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)


def init_shell(app: Quart):
    from .libs.gino import db
    from app.models.user import User
    from app.models.course import CourseStudent
    from app.models.chat_records import ChatRecords
    from app.models.subcribe import SubContent, SubUser

    @app.shell_context_processor
    def _():
        return {
            "db": db,
            "User": User,
            "CourseStudent": CourseStudent,
            "ChatRecords": ChatRecords,
            "SubContent": SubContent,
            "SubUser": SubUser,
        }


def init() -> NoneBot:
    config = load_config()
    _bot = init_bot(config)
    _bot.server_app.before_serving(init_db)
    _bot.server_app.before_serving(init_cache)
    _bot.server_app.before_serving(init_scheduler)
    app = _bot.asgi
    register_blueprint(app)
    init_shell(app)
    return _bot
