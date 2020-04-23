# NoneBot 版教务处机器人

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

接收用户指令后执行相应教务处查询动作。

> nonebot 参考手册：  
> <https://nonebot.cqp.moe>

## 安装

先安装

```shell
poetry install
```

## 配置

### 创建环境变量

在项目根目录下创建 `.env` 文件，里面填相应的环境变量。

```ini
# nonebot 启动相关
HOST=0.0.0.0
PORT=8080
ENCRYPT_KEY=xxxx # 加密的key
T_CN_SOURCE=xxxx # 请求新浪短网址的 key
API_URL=xxx # 后端 API 地址
WEB_URL=xxx # WEB 页面地址
QQAI_APPID=xxx # 语音识别调用时候会用到
QQAI_APPKEY=xxx # 同上
SUPERUSERS=xxxx,xxxx # 管理员qq，逗号分隔
QUART_APP=run:app
QUART_DEBUG=True

# cqhttp docker 启动相关
COOLQ_ACCOUNT=xxxxx # 要登陆的 QQ 号
VNC_PASSWD=xxx # vnc 密码
COOLQ_DIR=xxx # coolq 的目录

# 数据库相关信息
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=qqrobot
PGADMIN_DEFAULT_EMAIL=user@domain.com
PGADMIN_DEFAULT_PASSWORD=password
```

### 启动

需要先配置 `.env`。  
需要先配置 `.env`。  
需要先配置 `.env`。  

配置数据库：

```sh
docker-compose run --rm nonebot alembic upgrade head
```

需要等执行完，第一次比较慢，因为需要 build 镜像，之后就快很多了。

然后运行：

```sh
docker-compose up -d --no-recreate
```

想更新的时候执行：

```sh
docker-compose pull
```

## 语音识别

识别使用的是 <https://ai.qq.com> 的 API，你需要自己去申请一个密钥，填入 .env 即可。
你需要先在环境变量中设置 `COOLQ_DIR`，这样机器人才能读取到语音文件。

## 更新数据库

如果 container 已经在运行中的话，可以使用 `exec`：

```sh
docker-compose exec nonebot alembic revision --autogenerate -m 'message'
```

没运行的话可以执行：

```sh
docker-compose run --rm nonebot alembic revision --autogenerate -m 'message'
```

### 其他相关

fix `Target database is not up to date.`:

同上所述，container 运行中可以使用：

```sh
docker-compose exec nonebot alembic stamp heads
```

否则：

```sh
docker-compose run --rm nonebot alembic stamp heads
```

更新数据库：

```sh
docker-compose exec nonebot alembic upgrade head
```
