# 全局 Log
import logging
from logging import handlers
from nonebot.log import logger
import sys

IS_LOGGER = logging.getLogger("iswust")
IS_LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "[%(asctime)s %(name)s] %(levelname)s: [%(filename)s %(funcName)s] > %(message)s"
)
handler.setFormatter(formatter)
# 往文件里写入 指定间隔时间自动生成文件的处理器
# 实例化TimedRotatingFileHandler
# interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除
# when是间隔的时间单位，单位有以下几种：
# S 秒 M 分 H 小时、 D 天、 W 每星期（interval==0时代表星期一）
fh = handlers.TimedRotatingFileHandler(
    filename="iswust.log", when="D", backupCount=30, encoding="utf-8"
)
fh.setFormatter(formatter)

IS_LOGGER.addHandler(handler)
IS_LOGGER.addHandler(fh)

fh1 = handlers.TimedRotatingFileHandler(
    filename="nonebot.log", when="D", backupCount=30, encoding="utf-8"
)
fh1.setFormatter(formatter)
logger.addHandler(fh1)
