# 全局 Log
import logging
import sys

IS_LOGGER = logging.getLogger("iswust")
IS_LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "[%(asctime)s %(name)s] %(levelname)s: [%(filename)s %(funcName)s] > %(message)s"
)
handler.setFormatter(formatter)

IS_LOGGER.addHandler(handler)
