from . import api
from nonebot import CQHttpError
import nonebot as nb
bot = nb.get_bot()
from quart import request, jsonify


@api.route('/push', methods=["GET"])
async def push():
    query = request.args
    qq_ = query.get('qq')
    msg_ = query.get('msg')
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
