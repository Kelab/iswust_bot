from datetime import timedelta
from sqlalchemy.engine.url import URL

from .env import env

__all__ = ["get_database_url", "MyConfig"]


def get_database_url() -> URL:
    port = 5432
    if env("RUN_MODE", "") != "bot":
        port = env("DATABASE_PORT", 5432)
    return URL(
        host=env("DATABASE_HOST", "database"),
        port=port,
        drivername="postgresql",
        username=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
        database=env("POSTGRES_DATABASE", "qqrobot"),
    )


class MyConfig:
    SUPERUSERS = env.list("SUPERUSERS", "", subcast=int)
    HOST = env("HOST", "0.0.0.0")
    PORT = env("PORT", 8080)
    DEBUG = env("DEBUG", False)
    NICKNAME = {"小科", "小助手", "助手"}
    COMMAND_START = {"", "/", "\\"}
    COMMAND_SEP = {"|", "."}
    DATABASE_URL = get_database_url()
    SESSION_RUN_TIMEOUT = timedelta(minutes=2)
    SECRET = env("SECRET")
    AIOCACHE_DEFAULT_CONFIG = {
        "cache": "aiocache.SimpleMemoryCache",
        "serializer": {"class": "aiocache.serializers.PickleSerializer"},
    }
    SUBSCIBE_INTERVAL = env.int("SUBSCIBE_INTERVAL", 600)  # 单位 s
    DB_ECHO = env.bool("DB_ECHO", False)
