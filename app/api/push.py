import json
import nonebot as nb

from quart import jsonify, request
from typing import Optional
from nonebot import CQHttpError

from . import api
from log import IS_LOGGER
from utils.tools import bot_hash, check_args

bot = nb.get_bot()


@api.route('/push', methods=["GET", "POST"])
async def push():
    if request.method == 'GET':
        query: dict = request.args
        qq_: Optional[str] = query.get('qq')
        msg_: Optional[str] = query.get('msg')
        token_: Optional[str] = query.get('token')

    else:
        query: dict = json.loads(await request.get_data())
        qq_: Optional[str] = query.get('qq')
        msg_: Optional[str] = query.get('msg')
        token_: Optional[str] = query.get('token')

    result, msg = check_args(qq=qq_, msg=msg_, token=token_)

    rcode_ = 403
    rmsg_ = msg

    if result:
        if qq_ and msg_:
            encrypt_qq = bot_hash(qq_)

            IS_LOGGER.info(
                f"qq: {qq_} msg: {msg_} token: {token_} encrypt_qq: {encrypt_qq}"
            )
            if token_ == encrypt_qq:
                try:
                    await bot.send_private_msg(user_id=qq_, message=msg_)
                    rcode_ = 200
                    rmsg_ = "发送成功"
                except CQHttpError:
                    rcode_ = 500
                    rmsg_ = "向用户发消息失败！"
                bot._server_app.config['JSONIFY_MIMETYPE'] = "text/html"
                return jsonify(code=rcode_, data=None, msg=rmsg_)
            else:
                rmsg_ = "验证信息错误"
    IS_LOGGER.info(f"rcode_: {rcode_} rmsg_: {rmsg_}")
    return jsonify(code=rcode_, data=None, msg=rmsg_)
