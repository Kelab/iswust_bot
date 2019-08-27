import nonebot as nb
from . import api
from quart import request, jsonify
from nonebot import CQHttpError
from typing import Optional
bot = nb.get_bot()


@api.route('/push', methods=["GET"])
async def push():
    query: dict = request.args
    qq_: Optional[str] = query.get('qq')
    msg_: Optional[str] = query.get('msg')
    rcode_ = 403
    rmsg_ = ""
    try:
        if qq_ and msg_:
            await bot.send_private_msg(user_id=qq_, message=msg_)
            rcode_ = 200
            rmsg_ = "发送成功"
    except CQHttpError:
        rcode_ = 500
        rmsg_ = "发送失败"
    bot._server_app.config['JSONIFY_MIMETYPE'] = "text/html"
    return jsonify(code=rcode_, data=None, msg=rmsg_)
