import asyncio
import re
from importlib import import_module
from os import listdir, path

from gino.api import Gino as _Gino
from gino.api import GinoExecutor as _Executor
from gino.engine import GinoConnection as _Connection
from gino.engine import GinoEngine as _Engine
from gino.strategies import GinoStrategy

from loguru import logger
from nonebot import get_bot

from quart.exceptions import NotFound


class QuartModelMixin:
    @classmethod
    async def get_or_404(cls, *args, **kwargs):
        rv = await cls.get(*args, **kwargs)  # type: ignore
        if rv is None:
            raise NotFound()
        return rv


class GinoExecutor(_Executor):
    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound()
        return rv


class GinoConnection(_Connection):
    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound()
        return rv


class GinoEngine(_Engine):
    connection_cls = GinoConnection

    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound()
        return rv


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

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    async def first_or_404(self, *args, **kwargs):
        rv = await self.first(*args, **kwargs)
        if rv is None:
            raise NotFound()
        return rv

    async def set_bind(self, bind, loop=None, **kwargs):
        kwargs.setdefault("strategy", "quart")
        return await super().set_bind(bind, loop=loop, **kwargs)


db = Gino()


def load_models():
    """在创建数据表之前，加载 models 下面的所有数据表
    """
    module_prefix = "app.models"
    model_dir = path.join(path.dirname(__file__), "..", "models")
    for model in listdir(model_dir):
        model_path = path.join(model_dir, model)
        if path.isfile(model_path) and (
            model.startswith("_") or not model.endswith(".py")
        ):
            continue
        if path.isdir(model_path) and (
            model.startswith("_")
            or not path.exists(path.join(model_path, "__init__.py"))
        ):
            continue

        m = re.match(r"([_A-Z0-9a-z]+)(.py)?", model)
        if not m:
            continue
        module_name = f"{module_prefix}.{m.group(1)}"
        try:
            import_module(module_name)
            logger.info(f'Load model: "{module_name}"')
        except Exception as e:
            logger.error(f'Failed to Load "{module_name}", error: {e}')
            logger.exception(e)


async def init_db():
    logger.debug("Initializing database")
    bot = get_bot()
    app = bot.asgi
    if getattr(bot.config, "DATABASE_URL", None):
        try:
            db
            load_models()
            await db.set_bind(
                bot.config.DATABASE_URL,
                echo=app.config.setdefault("DB_ECHO", False),
                min_size=app.config.setdefault("DB_POOL_MIN_SIZE", 5),
                max_size=app.config.setdefault("DB_POOL_MAX_SIZE", 10),
                loop=asyncio.get_event_loop(),
                **app.config.setdefault("DB_KWARGS", dict()),
            )
            logger.info("Database connected")
        except Exception:
            raise ConnectionError("Database connection error!")
    else:
        logger.warning("DATABASE_URL is missing, database may not work")
