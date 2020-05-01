from datetime import timedelta
from .utils.env import env
from sqlalchemy.engine.url import URL


def get_database_url() -> URL:
    return URL(
        host="database",
        drivername="postgresql",
        username=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
        database=env("POSTGRES_DATABASE", "qqrobot"),
    )


def get_super_users() -> set:
    return env.list("SUPERUSERS", "", subcast=int)


class MyConfig:
    SUPERUSERS = get_super_users()
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
