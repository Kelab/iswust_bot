# iswust_nonebot

整合了很多功能的教务机器人

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> nonebot 参考手册：  
> <https://nonebot.cqp.moe>

致谢：

- Nonebot <https://github.com/nonebot/nonebot>
- 奶茶机器人 <https://github.com/cczu-osa/aki>
- ELF_RSS <https://github.com/Quan666/ELF_RSS>

---

## 配置

### 创建环境变量

复制一份 `.env.example` 重命名为 `.env`，并修改里面的内容。  

复制一份 `.quartenv.example` 重命名为 `.quartenv`，并修改里面的内容。  

### 启动

需要先[创建环境变量](#创建环境变量)。  
需要先[创建环境变量](#创建环境变量)。  
需要先[创建环境变量](#创建环境变量)。  

1. 首先 build 镜像：

    ```sh
    docker-compose build
    ```

    需要等执行完，build 阶段需要使用 pip 安装各种包比较慢。

2. 创建\更新 数据库结构：

    ```sh
    docker-compose run --rm nonebot alembic upgrade head
    ```

3. 然后运行：

    ```sh
    docker-compose up -d
    ```

想更新的时候执行：

```sh
docker-compose pull # 拉取依赖的镜像
docker-compose build # 重新打包
```

## 开发

如果想在本地开发还是需要安装开发环境的，用以 ide 的提示之类的。

```sh
poetry install
```

## 语音识别

识别使用的是 <https://ai.qq.com> 的 API，你需要自己去申请一个密钥，填入 .env 即可。

### docker 相关命令

#### 更新 poetry 依赖

```sh
docker-compose exec nonebot poetry install --no-interaction --no-dev
```

#### 查看运行日志

```sh
docker-compose logs -f --tail 10 nonebot
```

#### 执行数据库 migrate

```sh
# 如果 container 已经在运行中的话，可以使用 `exec`：
docker-compose exec nonebot alembic revision --autogenerate -m 'init'
# 没运行的话可以执行：
docker-compose run --rm nonebot alembic revision --autogenerate -m 'init'
```

#### 报错 `Target database is not up to date.`

```sh
# 同上所述，container 运行中可以使用：
docker-compose exec nonebot alembic stamp heads
# 否则：
docker-compose run --rm nonebot alembic stamp heads
```

#### 升级到最新数据库

```sh
# 如果 container 已经在运行中的话，可以使用 `exec`：
docker-compose exec nonebot alembic upgrade head
# 否则：
docker-compose run --rm nonebot alembic upgrade head
```

#### 删除本地数据库

先停止数据库，然后删除 `volume`：

```sh
docker-compose rm -s -v database
docker volume rm iswust_nonebot_database_data
# 再启动
docker-compose up -d database
docker-compose exec nonebot alembic upgrade head
```

或者直接删除所有东西，包括 `container`，`volume`：

```sh
docker-compose down -v --remove-orphans
```

#### 重启 nonebot

```sh
docker-compose restart nonebot
```
