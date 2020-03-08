import pickle
from auth_swust import request as requests, Login
from quart import abort, request

from app import db
from loguru import logger
from app.models import User
from app.utils.common import trueRet, falseRet
from app.utils.tools import bot_hash, check_args
from app.utils.parse.constants import API
from app.libs.aio import run_sync_func
from . import api


@api.route("/ecard", methods=["GET"])
async def ecard():
    qq = request.args.get("qq")
    token = request.args.get("token")

    result, msg = check_args(token=token, qq=qq)
    if not result:
        return falseRet(msg=msg)

    if bot_hash(qq) != token:
        abort(403)

    logger.info("qq {} 正在请求一卡通消费数据!".format(qq))

    u = User.query.filter_by(bind_qq=qq).first()
    if u is None:
        return falseRet(msg="no such user!")

    # 更新
    cookies = pickle.loads(u.cookies)
    sess = requests.Session(cookies)
    res = await run_sync_func(
        sess.get, API.jwc_index, allow_redirects=False, verify=False
    )
    # 302重定向了，session失效，刷新
    if res.status_code == 302 or res.status_code == 301:
        logger.info("qq {} 的session 失效".format(qq))
        logger.debug("load ID--{} password--{}".format(u.student_card, u.password))
        u_ = Login(u.student_card, u.password)
        is_log, log_resp = u_.try_login()
        if is_log:
            u.cookies = pickle.dumps(u_.get_cookies())
            db.session.add(u)
            db.session.commit()
            sess.cookies = u_.get_cookies()
        else:
            # 日志记录
            return falseRet(msg=log_resp)

    res = sess.get(
        f"http://my.swust.edu.cn/mht_shall/a/service/cardData?stuempno={u.student_card}"
    )

    return trueRet(data=res.json())
