from os import path
from typing import Any

import nonebot as nb
from nonebot import NoneBot, default_config
from quart import Quart

from .libs.gino import init_db
from .libs.cache import init_cache

from .utils.roconfig import Configuration


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

    return conf.to_config()


def register_blueprint(app: Quart):
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)


def init() -> NoneBot:
    config = load_config()
    _bot = init_bot(config)
    _bot.server_app.before_serving(init_db)
    _bot.server_app.before_serving(init_cache)
    app = _bot.asgi
    register_blueprint(app)
    return _bot
