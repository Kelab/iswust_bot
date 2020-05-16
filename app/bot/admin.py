from nonebot import CommandSession, get_bot, on_command
import nonebot.permission as perm
from nonebot.command import CommandManager
import pprint


@on_command("get_configs", aliases=["设置"], permission=perm.SUPERUSER)
async def get_config(session: CommandSession):
    await session.send(f"{pprint.pformat(get_bot().config.__dict__, indent=2)}")


@on_command("get_commands", aliases=["命令"], permission=perm.SUPERUSER)
async def get_command(session: CommandSession):
    await session.send(f"{pprint.pformat(CommandManager().commands, indent=2)}")
