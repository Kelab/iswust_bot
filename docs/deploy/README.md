# 部署

## 配置环境变量

复制一份 `.env.example` 重命名为 `.env`，并修改里面的内容。  

复制一份 `.quartenv.example` 重命名为 `.quartenv`，并修改里面的内容。  

各字段的意义文件内都有，也可在侧边栏配置项中查看详细信息。

## 启动

需要先[配置环境变量](#配置环境变量)。  
需要先[配置环境变量](#配置环境变量)。  
需要先[配置环境变量](#配置环境变量)。  

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

然后浏览器打开地址 `localhost:${CQHTTP_PORT}` 进入 `noVNC`，这个 `CQHTTP_PORT` 是你配置在 `.env` 里的。
输入你配置在 `.env` 内的密码，然后登录你的 QQ 小号即可。

添加 QQ 小号为好友即可使用各种[功能](/guide/)。
