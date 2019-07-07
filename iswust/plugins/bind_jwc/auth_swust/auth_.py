import os
import time
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image

import tensorflow as tf
from .captcha_recognition import predict_captcha
from .headers import headers
from .constants import URL

# 如果你使用tensorflow CPU方式也不要删去下面配置部分。

# 定义TensorFlow配置
config = tf.compat.v1.ConfigProto()
# 配置GPU内存分配方式，按需增长，很关键
config.gpu_options.allow_growth = True
# 配置可使用的显存比例
config.gpu_options.per_process_gpu_memory_fraction = 0.1
# 在创建session的时候把config作为参数传入
sess = tf.compat.v1.Session(config=config)
# 设置Keras的session
tf.compat.v1.keras.backend.set_session(sess)

# 设置model的位置
path = os.path.split(os.path.realpath(__file__))[0]
model_path = os.path.join(path, r'captcha_recognition\model\captcha.model')
print("model_path:", model_path)
# 设置计算图
graph = tf.compat.v1.get_default_graph()

# 加载模型
model = tf.compat.v1.keras.models.load_model(model_path)


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        _sess = requests.session()
        _sess.headers = headers
        self.sess = _sess

        self.cap_code = None
        self.post_data = None
        self.res = None
        self.hidden = None

    def get_init_sess(self, url):
        self.res = self.sess.get(url)

    def get_auth_sess(self):
        post_data = {
            "username": self.username,
            "password": self.password,
            "rememberMe": "on",
            "captchaResponse": self.cap_code,
            "lt": self.hidden[0].attrs['value'],
            "dllt": self.hidden[1].attrs['value'],
            "execution": self.hidden[2].attrs['value'],
            "_eventId": "submit",
            "rmShown": '1'
        }
        self.post_data = post_data
        self.sess.post(URL.index_url, data=self.post_data)
        print(post_data)

    def parse_hidden(self):
        bs = BeautifulSoup(self.res.text, "lxml")

        self.hidden = bs.select('#casLoginForm > input[type="hidden"]')

    def get_cap(self):
        cap = self.sess.get(URL.captcha_url)

        imgBuf = BytesIO(cap.content)

        im = Image.open(imgBuf)

        # 验证码识别
        # 使用 with 关键字防止内存溢出
        with graph.as_default():
            with sess.as_default():
                code = predict_captcha(im, model)
                if code:
                    self.cap_code = code

    # 检查是否登陆成功
    def check_success(self):
        res = self.sess.get(URL.student_info_url, allow_redirects=False)
        if res.status_code == 302:
            return False
        else:
            return True

    def try_login(self):
        self.get_init_sess(URL.index_url)
        self.get_cap()
        self.parse_hidden()
        self.get_auth_sess()
        if self.check_success():
            return self.sess
        else:
            # 重试5次，如果还是失败的话就返回False
            for x in range(5):
                print("重试登录：第 --", x + 1, "-- 次")
                # 减小频率，减轻教务处压力
                time.sleep(0.3)
                self.get_cap()
                self.get_auth_sess()
                if self.check_success():
                    return self.sess
            return False

    def get_cookie_jar_obj(self):
        return self.sess.cookies
