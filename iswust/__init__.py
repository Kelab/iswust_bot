from os import path
from typing import Any

import nonebot as nb
from . import db


def init(config_object: Any) -> nb.NoneBot:

    nb.init(config_object)
    bot = nb.get_bot()

    # 数据库连接
    bot.server_app.before_serving(db.init)

    nb.load_builtin_plugins()
    nb.load_plugins(path.join(path.dirname(__file__), 'plugins'),
                    'iswust.plugins')

    return bot
