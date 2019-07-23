import nonebot as nb
from typing import Any


def init(bot: nb.NoneBot, config: Any) -> nb.NoneBot.asgi:
    app = bot.asgi

    @app.route('/admin')
    async def admin():
        try:
            for user in config.SUPERUSERS:
                await bot.send_private_msg(user_id=user, message='Admin')
        except nb.CQHttpError:
            pass

        return 'This is the admin page.'

    @app.route('/push')
    async def push():
        return 'push'

    return app
