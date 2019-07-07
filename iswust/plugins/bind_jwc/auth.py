import pickle
from .auth_swust import Login
from .models import User


async def login_jwc(username: str, password: str, ctx: dict) -> bool:
    sender = ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    # 检查用户名和密码的长度
    if len(username) >= 6 and len(password) >= 6:
        user_query = await User.query.where(User.qq == sender_qq).gino.first()
        print(user_query)
        # 用户不存在，增加
        if not user_query:
            new_user = User(username=username, password=password, qq=sender_qq)

            # 模拟登陆，拿到cookie
            login = Login(username, password)
            sess = login.try_login()
            # 如果登陆成功
            if sess:
                new_user.usrObj = str(pickle.dumps(login.get_cookie_jar_obj()))
                await new_user.create()
                return True
            # 重试5次后失败
            else:
                msg = '绑定失败，请检查用户密码是否正确，检查教务处连接是否正常!'
                return msg
        else:
            # 用户存在
            msg = "你已经绑定~"
            return msg
    else:
        msg = "输入帐号密码格式错误!"
        return msg
