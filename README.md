# NoneBot 版教务处机器人
接收用户指令后执行相应教务处查询动作。
请了解代码后再使用。


## 安装
先安装
```shell
pip install -r requirements.txt
```

启动 `bot.py` 即可·


## 创建环境变量
在项目根目录下创建 `.env` 文件，里面填相应的环境变量。
```
ENCRYPT_KEY=xxxx # 加密的key
T_CN_SOURCE=xxxx # 请求新浪短网址的 key
AN_HAO=xxxx # 处理加好友请求的暗号
API_URL=xxx # 后端 API 地址
WEB_URL=xxx # WEB 页面地址
```

## 相关包
- [auth_swsut](https://github.com/BuddingLab/auth_swust)
- [time_converter](https://github.com/BuddingLab/time_converter)