from gino import Gino
from nonebot import get_bot

db = Gino()


async def init() -> None:
    """
    Initialize database module.
    """
    bot = get_bot()
    if getattr(bot.config, 'DATABASE_URL', None):
        await db.set_bind(bot.config.DATABASE_URL)
        print('Database connected')
    else:
        print('DATABASE_URL is missing, database may not work')
