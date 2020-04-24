import os
from pathlib import Path
from loguru import logger
from nonebot.log import logger as nblogger
from logging import handlers, Formatter

_dir_name = "logs"
if not os.path.exists(_dir_name):
    os.mkdir(_dir_name)
log_dir = Path(_dir_name)

# 往文件里写入 指定间隔时间自动生成文件的处理器
# 实例化TimedRotatingFileHandler
# interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除
# when是间隔的时间单位，单位有以下几种：
# S 秒 M 分 H 小时、 D 天、 W 每星期（interval==0时代表星期一）
fh = handlers.TimedRotatingFileHandler(
    filename=str(log_dir / "nonebot.log"), when="D", backupCount=30, encoding="utf-8",
)
fh.setFormatter(
    Formatter(
        "[%(asctime)s %(name)s] %(levelname)s: [%(filename)s %(funcName)s] > %(message)s"
    )
)
nblogger.addHandler(fh)


logger.add(
    str(log_dir / "iswust_{time:YYYY-MM-DD}.log"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation="12:00",
    enqueue=True,
    encoding="utf-8",
    level="DEBUG",
    compression="zip",
    retention="10 days",
)
