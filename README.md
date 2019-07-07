# NoneBot 版教务处机器人

先安装
```shell
pip install -r requirements.txt
```


启动 `bot.py` 即可·

## 创建数据库
第一个要做的就是创建数据库
```shell
# 从版本 创建数据库表结构
alembic upgrade head
```

如果你更新了数据表结构，在 `alembic/env.py` 里的 `target_metadata` 写好，然后执行：
```shell
# 从 models 中生成数据表版本
alembic revision --autogenerate -m "message"
# 从版本 创建数据库表结构
alembic upgrade head
```