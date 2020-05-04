import pickle
from quart import request, abort
from auth_swust import Login, request as requests

from app.libs.gino import db
from loguru import logger
from app.models.user import User
from app.models.course import Course
from app.utils.common import trueRet, falseRet
from app.utils.tools import bot_hash, check_args
from app.libs.aio import run_sync_func
from .parse.constants import API


async def getCourse_util(func):
    async def wrapper():
        qq = request.args.get("qq")
        token = request.args.get("token")
        update = request.args.get("update")

        result, msg = check_args(token=token, qq=qq)
        if not result:
            return falseRet(msg=msg)

        if bot_hash(qq) != token:
            abort(403)

        u = User.query.filter_by(bind_qq=qq).first()
        if u is None:
            return falseRet(msg="no such user!")

        if not update:
            # 直接从数据库里面取
            cour = Course.query.filter_by(uid=u.uid).first()
            if cour is not None:
                return trueRet(data=pickle.loads(cour.course_table))

        # 更新
        cookies = pickle.loads(u.cookies)
        sess = requests.Session(cookies)
        res = await run_sync_func(
            sess.get, API.jwc_index, allow_redirects=False, verify=False
        )
        # 302重定向了，session失效，刷新
        if res.status_code == 302 or res.status_code == 301 or update:
            logger.info("qq {} 的session 失效".format(qq))
            logger.debug("load ID--{} password--{}".format(u.student_card, u.password))

            u_ = Login(u.student_card, u.password)
            is_log, log_resp = await run_sync_func(u_.try_login)
            if is_log:
                u.cookies = pickle.dumps(u_.get_cookies())
                db.session.add(u)
                db.session.commit()
                return func(cookies=u_.get_cookies(), uid=u.uid)
            else:
                # 日志记录
                return falseRet(msg=log_resp)
        else:
            return func(cookies=cookies, uid=u.uid)

    return wrapper
