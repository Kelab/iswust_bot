from os import getenv as _
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    user = _("POSTGRES_USER")
    passwd = _("POSTGRES_PASSWORD")
    db = _("POSTGRES_DB")
    if user and passwd and db:
        return f"postgresql://{user}:{passwd}@database/{db}"
    return ""


def get_super_users() -> set:
    # TODO use database
    return set(map(int, _("SUPERUSERS", "").split(",")))


class MyConfig:
    SUPERUSERS = get_super_users()
    HOST = _("HOST") or "0.0.0.0"
    PORT = _("PORT") or "8080"
    DEBUG = _("DEBUG") or False
    NICKNAME = {"小科", "小助手", "助手"}
    COMMAND_START = {"", "/", "\\"}
    COMMAND_SEP = {"|", "."}
    DATABASE_URL = get_database_url()
    SESSION_RUN_TIMEOUT = timedelta(seconds=20)
    AIOCACHE_DEFAULT_CONFIG = {
        "cache": "aiocache.SimpleMemoryCache",
        "serializer": {"class": "aiocache.serializers.PickleSerializer"},
    }
