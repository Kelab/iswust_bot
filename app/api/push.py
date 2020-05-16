import json
from typing import Optional

import nonebot as nb
from loguru import logger
from nonebot import CQHttpError
from quart import jsonify, request

from app.utils.tools import bot_hash, check_args

from . import api


@api.route("/push", methods=["GET", "POST"])
async def push():
    bot = nb.get_bot()
    if request.method == "GET":
        query: dict = request.args
        qq_: Optional[str] = query.get("qq")
        msg_: Optional[str] = query.get("msg")
        token_: Optional[str] = query.get("token")

    else:
        query: dict = json.loads(await request.get_data())
        qq_: Optional[str] = query.get("qq")
        msg_: Optional[str] = query.get("msg")
        token_: Optional[str] = query.get("token")

    result, msg = check_args(qq=qq_, msg=msg_, token=token_)

    rcode_ = 403
    rmsg_ = msg

    if result and qq_:
        encrypt_qq = bot_hash(qq_)

        logger.info(f"qq: {qq_} msg: {msg_} token: {token_} encrypt_qq: {encrypt_qq}")
        if token_ == encrypt_qq:
            try:
                await bot.send_private_msg(user_id=qq_, message=msg_)
                rcode_ = 200
                rmsg_ = "发送成功"
            except CQHttpError:
                rcode_ = 500
                rmsg_ = "向用户发消息失败！"
            bot._server_app.config["JSONIFY_MIMETYPE"] = "text/html"
        else:
            rmsg_ = "验证信息错误"
    logger.info(f"rcode_: {rcode_} rmsg_: {rmsg_}")
    return jsonify(code=rcode_, msg=rmsg_)
