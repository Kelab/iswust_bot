import nonebot as nb
import json
from . import api
from quart import request, jsonify
from nonebot import CQHttpError
from utils.tools import xor_decrypt, check_args
from typing import Optional
from log import IS_LOGGER
bot = nb.get_bot()


@api.route('/push', methods=["GET", "POST"])
async def push():
    if request.method == 'GET':
        query: dict = request.args
        qq_: Optional[str] = query.get('qq')
        msg_: Optional[str] = query.get('msg')
        verifycode_: Optional[str] = query.get('verifycode')

    else:
        query: dict = json.loads(await request.get_data())

        qq_: Optional[str] = query.get('qq')
        msg_: Optional[str] = query.get('msg')
        verifycode_: Optional[str] = query.get('verifycode')

    decrypt_qq: Optional[int] = None

    result, msg = check_args(qq=qq_, msg=msg_, verifycode=verifycode_)

    rcode_ = 403
    rmsg_ = msg

    if result:
        if verifycode_:
            decrypt_qq = xor_decrypt(int(verifycode_))
        else:
            IS_LOGGER.error('missing params: verifycode')

        IS_LOGGER.info(
            f"qq: {qq_} msg: {msg_} verifycode: {verifycode_} decrypt_qq: {decrypt_qq}"
        )
        if qq_ and msg_:
            if decrypt_qq == int(qq_):
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
