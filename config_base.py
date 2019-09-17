from nonebot.default_config import timedelta
from nonebot.default_config import *

SUPERUSERS = {}
HOST = '0.0.0.0'
PORT = 8080

NICKNAME = {}
COMMAND_START = {}
COMMAND_SEP = {}
SESSION_RUN_TIMEOUT = timedelta(seconds=20)

# 用户取消交互时的回复
SESSION_CANCEL_EXPRESSION = ('好的', '好的吧', '好吧，那就不打扰啦')
