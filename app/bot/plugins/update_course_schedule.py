from nonebot import CommandSession, on_command
from requests import Response

from app.bot.constants.config import api_url
from utils.aio import requests
from utils.tools import bot_hash

__plugin_name__ = '更新课表'
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()

