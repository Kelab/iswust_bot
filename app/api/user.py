import pickle

from auth_swust import Login
from loguru import logger
from nonebot import get_bot
from quart import abort, request

from app.libs.aio import run_sync_func
from app.models.user import User
from app.utils.bot_common import qq2event
from app.utils.common import falseRet, trueRet
from app.utils.tools import bot_hash, check_args

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
    user = await User.get(str(qq))

    _bot = get_bot()
    if user is None:
        logger.info("qq{}是新用户,正在尝试登录教务处...".format(qq))
        u = Login(username, password)
        is_log, log_resp = await run_sync_func(u.try_login)
        if is_log:
            user_info = await run_sync_func(log_resp.json)
            logger.debug(user_info)
            await logger.complete()

            await User.add(
                qq=qq,
                student_id=username,
                password=password,
                cookies=pickle.dumps(u.get_cookies()),
            )
            logger.info("qq{}绑定成功!".format(qq))
            await _bot.send(qq2event(qq), "教务处绑定成功！")
            await _bot.send(qq2event(qq), "可以向我发送 帮助 来继续使用~")
            return trueRet("qq绑定成功!")
        else:
            logger.info("qq{}绑定失败!".format(qq))
            await _bot.send(qq2event(qq), "教务处绑定失败！")
            return falseRet("qq绑定失败!失败原因是{}".format(log_resp))
    return falseRet("该qq已经绑定了!")


@api.route("/user/unbind")
async def unbind():
    qq = request.args.get("qq")
    token = request.args.get("token")
    result, msg = check_args(qq=qq, token=token)

    if bot_hash(qq) != token:
        abort(403)
    if not result:
        return falseRet(msg=msg)

    logger.info("qq {}正在请求解绑!".format(qq))

    try:
        User.unbind(qq)
        logger.info("qq {}请求解绑成功!".format(qq))
        return trueRet(msg="解除绑定成功!")
    except Exception as e:
        logger.exception(e)

    return falseRet(msg="没有这个用户!")
