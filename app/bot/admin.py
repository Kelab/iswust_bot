from typing import Callable, Awaitable
from nonebot import CommandSession, get_bot, on_command
import nonebot.permission as perm
from nonebot.message import unescape
import pprint


@on_command("get_config", permission=perm.SUPERUSER)
async def get_config(session: CommandSession):
    await session.send(f"执行中： {get_bot().config.__dict__}")


@on_command("exec", permission=perm.SUPERUSER)
async def exec_(session: CommandSession):
    await session.send(f"执行中： {session}")
    code = unescape(session.current_arg)
    try:
        tmp_locals = {}
        exec(code, None, tmp_locals)
        await session.send(f"Locals：\n{pprint.pformat(tmp_locals, indent=2)}")
        if isinstance(tmp_locals.get("run"), Callable):
            res = tmp_locals["run"](session.bot, session.ctx)
            if isinstance(res, Awaitable):
                res = await res
            await session.send(f"执行成功\n" f"返回：\n{pprint.pformat(res, indent=2)}")
    except Exception as e:
        await session.send(f"执行失败\n异常：\n{pprint.pformat(e, indent=2)}")
        return
