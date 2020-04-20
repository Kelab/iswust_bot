import pickle
from auth_swust import request

from app.libs.gino import db
from app.models.course import Course
from app.utils.common import trueRet
from app.utils.course import getCourse_util
from app.utils.parse.parse_course_table import get_course_api
from . import api


@api.route("/course/getCourse", methods=["GET"])
@getCourse_util
def getCourse(cookies, uid):
    # 如果不更新,就从数据库里面取,如果更新就重新请求
    sess = request.Session()
    sess.cookies = cookies
    res = get_course_api(sess)

    # 没有就增加
    course = Course.query.filter_by(uid=uid).first()
    if not course:
        course = Course(uid=uid, course_table=pickle.dumps(res))
    # 有就更新
    else:
        course.course_table = pickle.dumps(res)

    db.session.add(course)
    db.session.commit()

    return trueRet(data=res)


@api.route("/course/depositIcs", methods=["GET"])
def depositIcs(cookies, uid):
    # 如果不更新,就从数据库里面取,如果更新就重新请求
    sess = request.Session()
    sess.cookies = cookies
    res = get_course_api(sess)

    # 没有就增加
    course = Course.query.filter_by(uid=uid).first()
    if not course:
        course = Course(uid=uid, course_table=pickle.dumps(res))
    # 有就更新
    else:
        course.course_table = pickle.dumps(res)

    db.session.add(course)
    db.session.commit()

    return trueRet(data=res)
