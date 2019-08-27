from . import api
from nonebot import CQHttpError
from log import BOT_LOGGER
import nonebot as nb
bot = nb.get_bot()


@api.route('/admin')
async def admin():
    try:
        BOT_LOGGER.info('请求了 admin 页面')
    except CQHttpError:
        pass

    return 'This is the admin page.'
