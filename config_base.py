from os import path
from nonebot.default_config import *

SUPERUSERS = {}
HOST = '0.0.0.0'
PORT = 8080
NICKNAME = {'小科', '小助手', '助手'}
COMMAND_START = {'', '/', '!', '／', '！'}
COMMAND_SEP = {'/', '.'}
SESSION_RUN_TIMEOUT = timedelta(seconds=20)

# 用户取消交互时的回复
SESSION_CANCEL_EXPRESSION = ('好的', '好的吧', '好吧，那就不打扰啦')

# 数据文件夹
DATA_FOLDER = path.join(path.dirname(__file__), 'data')

# 数据库 URL
DATABASE_URL = ''
