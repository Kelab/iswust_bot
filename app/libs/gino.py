import asyncio

from gino.api import Gino as _Gino
from gino.api import GinoExecutor as _Executor
from gino.engine import GinoConnection as _Connection
from gino.engine import GinoEngine as _Engine
from gino.strategies import GinoStrategy

from loguru import logger


class QuartModelMixin:
    pass


class GinoExecutor(_Executor):
    pass


class GinoConnection(_Connection):
    pass


class GinoEngine(_Engine):
    connection_cls = GinoConnection


class QuartStrategy(GinoStrategy):
    name = "quart"
    engine_cls = GinoEngine


QuartStrategy()


# noinspection PyClassHasNoInit
class Gino(_Gino):
    """Support Quart web server.
    By :meth:`init_app` GINO registers a few hooks on Quart, so that GINO could
    use database configuration in Quart ``config`` to initialize the bound
    engine.
    """

    model_base_classes = _Gino.model_base_classes + (QuartModelMixin,)
    query_executor = GinoExecutor

    async def set_bind(self, bind, loop=None, **kwargs):
        kwargs.setdefault("strategy", "quart")
        return await super().set_bind(bind, loop=loop, **kwargs)


db = Gino()


async def init_db():
    logger.debug("Initializing database")
    from app.config import MyConfig

    if getattr(MyConfig, "DATABASE_URL", None):
        try:
            await db.set_bind(
                MyConfig.DATABASE_URL,
                echo=MyConfig.DB_ECHO,
                loop=asyncio.get_event_loop(),
            )
            logger.info("Database connected")
        except Exception:
            raise ConnectionError("Database connection error!")
    else:
        logger.warning("DATABASE_URL is missing, database may not work")
