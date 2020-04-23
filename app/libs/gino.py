from contextlib import contextmanager

from gino import Gino as _Gino
from loguru import logger
from nonebot import get_bot
from importlib import import_module
from os import path, listdir
import re


class Gino(_Gino):
    pass


db = Gino()


def load_models():
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
    if getattr(bot.config, "DATABASE_URL", None):
        try:
            await db.set_bind(bot.config.DATABASE_URL)
            logger.info("Database connected")
        except Exception:
            raise ConnectionError("Database connection error!")
    else:
        logger.warning("DATABASE_URL is missing, database may not work")
