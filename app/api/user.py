import pickle
from auth_swust import Login
from quart import request, abort
from loguru import logger
from app.models.user import User
from app.utils.common import trueRet, falseRet
from app.utils.tools import check_args, bot_hash
from . import api


@api.route("/user/bind", methods=["POST"])
async def bind():
    res = await request.get_json()
    qq = res.get("qq")
    username = res.get("username")
    password = res.get("password")
    token = res.get("token")

    logger.debug("username:{} password:{} token:{}".format(username, password, token))

    result, msg = check_args(qq=qq, username=username, password=password, token=token)

    if bot_hash(qq) != token:
        abort(403)

    if not result:
        return falseRet(msg=msg)

    logger.info("qq{}正在请求绑定!".format(qq))
    # 是否已经绑定
    user = User.query.filter_by(bind_qq=qq).first()

    if user is None:
        logger.info("qq{}是新用户,正在尝试登录教务处...".format(qq))
        u = Login(username, password)
        is_log, log_resp = u.try_login()
        if is_log:
            logger.debug(log_resp.json())
            User.add(username, password, qq, pickle.dumps(u.get_cookies()))
            logger.info("qq{}绑定成功!".format(qq))
            return trueRet("qq绑定成功!")
        else:
            logger.info("qq{}绑定失败!".format(qq))
            return falseRet("qq绑定失败!失败原因是{}".format(log_resp))

    return falseRet("该qq已经绑定了!")


@api.route("/user/unbind")
def unbind():
    qq = request.args.get("qq")
    token = request.args.get("token")
    result, msg = check_args(qq=qq, token=token)

    if bot_hash(qq) != token:
        abort(403)
    if not result:
        return falseRet(msg=msg)

    logger.info("qq {}正在请求解绑!".format(qq))
    user_query = User.query.filter_by(bind_qq=qq).first()
    if user_query:
        User.remove(qq)
        logger.info("qq {}请求解绑成功!".format(qq))
        return trueRet(msg="解除绑定成功!")
    return falseRet(msg="没有这个用户!")
