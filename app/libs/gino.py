from contextlib import contextmanager

from gino import Gino as _Gino
from loguru import logger
from nonebot import get_bot


class Gino(_Gino):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = Gino()


async def init_db():
    logger.debug("Initializing database")
    bot = get_bot()
    if getattr(bot.config, "DATABASE_URL", None):
        await db.set_bind(bot.config.DATABASE_URL)
        logger.info("Database connected")
    else:
        logger.warning("DATABASE_URL is missing, database may not work")
