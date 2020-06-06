import pickle

from auth_swust import Login
from loguru import logger
from nonebot import get_bot
from quart import abort, request

from app.libs.aio import run_sync_func
from app.models.user import User
from app.utils.bot import qq2event, get_user_center
from app.utils.api import false_ret, true_ret, check_args, to_token

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

    if to_token(qq) != token:
        abort(403)

    if not result:
        return false_ret(msg=msg)

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
            await _bot.send(qq2event(qq), "点击 https://bot.artin.li 来查看帮助~")
            await _bot.send(
                qq2event(qq), f"点击个人中心可以配置更多： {get_user_center(qq2event(qq))}"
            )
            return true_ret("qq绑定成功!")
        else:
            logger.info("qq{}绑定失败!".format(qq))
            await _bot.send(qq2event(qq), "教务处绑定失败！")
            return false_ret("qq绑定失败!失败原因是{}".format(log_resp))
    return false_ret("该qq已经绑定了!")


@api.route("/user/unbind")
async def unbind():
    qq = request.args.get("qq")
    token = request.args.get("token")
    result, msg = check_args(qq=qq, token=token)

    if to_token(qq) != token:
        abort(403)
    if not result:
        return false_ret(msg=msg)

    logger.info("qq {}正在请求解绑!".format(qq))

    try:
        await User.unbind(qq)
        logger.info("qq {}请求解绑成功!".format(qq))
        return true_ret(msg="解除绑定成功!")
    except Exception as e:
        logger.exception(e)

    return false_ret(msg="没有这个用户!")
