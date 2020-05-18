from os import path
from loguru import logger

import nonebot as nb
from nonebot import default_config
from quart import Quart

__all__ = ["init"]


def load_config():
    from .libs.roconfig import Configuration
    from .config import Config

    conf = Configuration()
    conf.add_object(default_config)
    conf.add_object(Config)
    logger.info(conf.to_dict())
    return conf.to_config()


def init_bot() -> nb.NoneBot:
    config = load_config()
    nb.init(config)
    bot = nb.get_bot()

    nb.load_builtin_plugins()
    nb.load_plugins(path.join(path.dirname(__file__), "bot"), "app.bot")

    from .libs.gino import init_db
    from .libs.scheduler import init_scheduler

    bot.server_app.before_serving(init_db)
    bot.server_app.before_serving(init_scheduler)

    return bot


def register_blueprint(app: Quart):
    from .utils.tools import load_modules

    load_modules("app.api")
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)


def init_shell(app: Quart):
    from .libs.gino import db
    from app.models.user import User
    from app.models.course import CourseStudent
    from app.models.chat_records import ChatRecords
    from app.models.subscribe import SubContent, SubUser

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


def init(mode: str = "bot") -> Quart:
    from .env import load_env

    load_env(mode)

    if mode == "bot":
        _bot = init_bot()
        app = _bot.asgi
        register_blueprint(app)
    else:
        app = Quart(__name__)
        init_shell(app)
    return app
