import sys

from quart import Quart

from . import bot


def register_blueprint(app: Quart):
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)


def init() -> Quart:
    try:
        import bot_config as config
    except ImportError:
        print('There is no config file!', file=sys.stderr)
        exit(1)

    _bot = bot.init(config)
    app = _bot.asgi
    register_blueprint(app)
    return app
