from nonebot.default_config import timedelta
from nonebot.default_config import *

SUPERUSERS = {}
HOST = "0.0.0.0"
PORT = 8080

NICKNAME = {}
COMMAND_START = {"", "/", "／"}
COMMAND_SEP = {"/", ".", "|"}
SESSION_RUN_TIMEOUT = timedelta(seconds=60)
SESSION_RUNNING_EXPRESSION = "上一条命令正在运行中哦~"

# 用户取消交互时的回复
SESSION_CANCEL_EXPRESSION = ("好的", "好的吧", "好吧，那就不打扰啦")

# 数据库 URL
DATABASE_URL = "postgresql://postgres:xxxx@localhost:5432/xxxx"

# aiocache 配置
AIOCACHE_DEFAULT_CONFIG = {
    "cache": "aiocache.SimpleMemoryCache",
    "serializer": {"class": "aiocache.serializers.PickleSerializer"},
}
