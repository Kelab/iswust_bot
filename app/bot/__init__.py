from os import path
from typing import Any

import nonebot as nb


def init(config_object: Any) -> nb.NoneBot:

    nb.init(config_object)
    bot = nb.get_bot()

    nb.load_builtin_plugins()
    nb.load_plugins(path.join(path.dirname(__file__), "plugins"), "app.bot.plugins")

    return bot
