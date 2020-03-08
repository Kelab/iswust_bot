from aiocache import caches
from nonebot import get_bot


def init_cache() -> None:
    """
    Initialize the cache module.
    """
    bot = get_bot()
    caches.set_config({"default": bot.config.AIOCACHE_DEFAULT_CONFIG})
