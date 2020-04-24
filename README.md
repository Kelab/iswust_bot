# NoneBot 版教务处机器人

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> nonebot 参考手册：  
> <https://nonebot.cqp.moe>

致谢：

- 奶茶机器人 <https://github.com/cczu-osa/aki>

---

## 配置

### 创建环境变量

复制一份 `.env.example` 重命名为 `.env`，并修改里面的内容。  
复制一份 `.env.example` 重命名为 `.env`，并修改里面的内容。  
复制一份 `.env.example` 重命名为 `.env`，并修改里面的内容。  

### 启动

需要先配置 `.env`。  
需要先配置 `.env`。  
需要先配置 `.env`。  

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
    docker-compose up -d --no-recreate
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
你需要先在环境变量中设置 `COOLQ_DIR`，这样机器人才能读取到语音文件。

### 相关 docker 命令

#### 查看运行日志

```sh
docker-compose logs -f --tail 10 nonebot
```

#### 报错 `Target database is not up to date.`

同上所述，container 运行中可以使用：

```sh
docker-compose exec nonebot alembic stamp heads
```

否则：

```sh
docker-compose run --rm nonebot alembic stamp heads
```

#### 执行数据库 migrate

如果 container 已经在运行中的话，可以使用 `exec`：

```sh
docker-compose exec nonebot alembic revision --autogenerate -m 'message'
```

没运行的话可以执行：

```sh
docker-compose run --rm nonebot alembic revision --autogenerate -m 'message'
```

#### 升级到最新数据库

如果 container 已经在运行中的话，可以使用 `exec`：

```sh
docker-compose exec nonebot alembic upgrade head
```

否则：

```sh
docker-compose run --rm nonebot alembic upgrade head
```

#### 删除本地数据库

```sh
docker-compose down -v # 会清除所有 volume
```
