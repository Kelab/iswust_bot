import json
import requests
import pickle
import time
from ..constants.urls import API


def get_request_json(raw_data):
    for data in raw_data:
        return json.loads(data)


def get_wday():
    wday = time.localtime(time.time()).tm_wday
    return wday + 1


# def check_session(func):
#     '''
#     check session and refresh session
#     :return:
#     '''

#     def wrapper(r, qq):
#         user = User.query.filter_by(qq=qq).first()
#         cookie_jar = pickle.loads(user.usrObj)
#         res = requests.get(API.studentInfo,
#                            cookies=cookie_jar,
#                            allow_redirects=False)
#         # 302重定向了，session失效，刷新
#         if res.status_code == 302:
#             print('session 失效')
#             refresh_user = Login()
#             refresh_user.username = user.name
#             refresh_user.password = user.password
#             if refresh_user.try_login():
#                 user.usrObj = pickle.dumps(refresh_user.get_cookie_jar_obj())
#                 db.session.add(user)
#                 db.session.commit()
#                 return func(r, qq)
#             else:
#                 # 日志记录
#                 return func(r, qq)
#         else:
#             return func(r, qq)

#     return wrapper

# def check_need_bind(func):
#     '''
#     check user bind or not bind
#     :return:
#     '''

#     def wrapper(r, qq):
#         user = User.query.filter_by(qq=qq).first()
#         if user:
#             return func(r, qq)
#         else:
#             sdk = HTTPSDK(r)
#             msg = '你还没有绑定,请先绑定后再执行此操作!\n发送数字0获取绑定提示。'
#             sdk.sendPrivateMsg(qq, msg)
#             return sdk.send()

#     return wrapper
