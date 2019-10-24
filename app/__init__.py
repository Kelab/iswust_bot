import sys
from os import path
from typing import Any

import nonebot as nb
from nonebot import NoneBot
from quart import Quart


def init_bot(config_object: Any) -> nb.NoneBot:
    nb.init(config_object)
    bot = nb.get_bot()

    nb.load_builtin_plugins()
    nb.load_plugins(path.join(path.dirname(__file__), "bot"), "app.bot")

    return bot


def register_blueprint(app: Quart):
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)


def init() -> NoneBot:
    try:
        import bot_config as config
    except ImportError:
        print("There is no config file!", file=sys.stderr)
        exit(1)

    _bot = init_bot(config)
    app = _bot.asgi
    register_blueprint(app)
    return _bot
