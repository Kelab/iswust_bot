import pprint

import nonebot.permission as perm
from nonebot import CommandGroup, CommandSession, get_bot, on_command
from nonebot.command import CommandManager

from app.libs.cache import cache


@on_command("get_configs", aliases=["设置"], permission=perm.SUPERUSER)
async def get_config(session: CommandSession):
    await session.send(f"{pprint.pformat(get_bot().config.__dict__, indent=2)}")


@on_command("get_commands", aliases=["命令"], permission=perm.SUPERUSER)
async def get_command(session: CommandSession):
    await session.send(f"{pprint.pformat(CommandManager._commands, indent=2)}")
    await session.send(f"{pprint.pformat(CommandManager._aliases, indent=2)}")


cc = CommandGroup("cache", permission=perm.SUPERUSER)


@cc.command("set")
async def _(session: CommandSession):
    data = session.current_arg
    try:
        key, value = data.split()
        key = key.strip()
        value = value.strip()
        await cache.set(key, value)
    except Exception:
        await session.send("输入有误")


@cc.command("get")
async def _(session: CommandSession):
    data = session.current_arg
    data = data.strip()
    value = await cache.get(data)
    await session.send(value)
