import json
import nonebot as nb

from quart import jsonify, request
from typing import Optional
from nonebot import CQHttpError
from nonebot.command import call_command

from . import api
from log import IS_LOGGER
from utils.tools import bot_hash, check_args

bot = nb.get_bot()


@api.route("/push/cs/today", methods=["GET", "POST"])
async def push_cs_today():
    if request.method == "GET":
        query: dict = request.args
    else:
        query: dict = json.loads(await request.get_data())

    qq_: Optional[str] = query.get("qq")
    token_: Optional[str] = query.get("token")

    result, msg = check_args(qq=qq_, token=token_)

    rcode_ = 403
    rmsg_ = msg

    if result:
        encrypt_qq = bot_hash(qq_)

        IS_LOGGER.info(f"推送今日课表：qq: {qq_} token: {token_} encrypt_qq: {encrypt_qq}")
        if token_ == encrypt_qq:
            try:
                ctx = {"user_id": qq_}
                await call_command(bot, ctx, "cs", args={"today": True})
                rcode_ = 200
                rmsg_ = "发送成功"
            except CQHttpError:
                rcode_ = 500
                rmsg_ = "向用户发消息失败！"
            bot._server_app.config["JSONIFY_MIMETYPE"] = "text/html"
            return jsonify(code=rcode_, msg=rmsg_)
        else:
            rmsg_ = "验证信息错误"
    IS_LOGGER.info(f"rcode_: {rcode_} rmsg_: {rmsg_}")
    return jsonify(code=rcode_, msg=rmsg_)
