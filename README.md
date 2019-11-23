# NoneBot 版教务处机器人
接收用户指令后执行相应教务处查询动作。

> nonebot 参考手册：  
> https://nonebot.cqp.moe

## 安装
先安装
```shell
pip install -r requirements.txt
```
最下方还有两个包需要手动安装。


启动 `bot.py` 即可·

会加载代码根目录下的 `bot_config.py` 作为配置文件，你可以根据自己的需要配置。

## 创建环境变量
在项目根目录下创建 `.env` 文件，里面填相应的环境变量。
```
ENCRYPT_KEY=xxxx # 加密的key
T_CN_SOURCE=xxxx # 请求新浪短网址的 key
AN_HAO=xxxx # 处理加好友请求的验证消息
API_URL=xxx # 后端 API 地址
WEB_URL=xxx # WEB 页面地址
QQAI_APPID=xxx # 语音识别调用时候会用到
QQAI_APPKEY=xxx # 同上
COOLQ_DIR=xxx # coolq 的目录
```

## 语音识别
识别使用的是 <https://ai.qq.com> 的 API，你需要自己去申请一个密钥，填入 .env 即可。
你需要先在环境变量中设置 `COOLQ_DIR`，这样机器人才能读取到语音文件。

## 相关包
- [auth_swsut](https://github.com/BuddingLab/auth_swust)
- [time_converter](https://github.com/BuddingLab/time_converter)
