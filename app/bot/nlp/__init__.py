from typing import Any, Dict, Tuple

from loguru import logger
from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot.permission import check_permission
from nonebot.command import CommandManager, Command
from rapidfuzz import fuzz, process


def gen_commands_keys(commands: Dict[Tuple, Any]):
    result_set = set()
    for item in commands.keys():
        if len(item) == 1:
            result_set.add(item[0])
    return result_set


@on_natural_language()
async def _(session: NLPSession):
    # 获取所有命令作为一个集合
    commands = CommandManager._commands  # type: Dict[Tuple, Command]
    aliases = CommandManager._aliases  # type: Dict[str, Command]

    choices = gen_commands_keys(commands)
    choices |= set(aliases.keys())

    raw_message = session.event.raw_message.split()
    # 假设该消息为命令，取第一个字段
    query_cmd = raw_message[0]
    result = process.extractOne(query_cmd, choices, scorer=fuzz.WRatio)
    if result:
        cmd, confidence = result
        if not check_permission(session.bot, session.event, commands[cmd].permission):
            # 用户没有权限执行
            return
        logger.debug(f"query_cmd: {query_cmd}")
        logger.debug(f"fuzz cmd, confidence: {cmd} {confidence}")
        if confidence - 66 > 0:
            raw_message[0] = cmd
            return IntentCommand(
                confidence, "switch", current_arg=" ".join(raw_message),
            )
