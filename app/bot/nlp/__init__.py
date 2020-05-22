from typing import Any, Dict, Tuple

from loguru import logger
from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot.command import CommandManager
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
    commands = CommandManager._commands  # type: Dict[Tuple, Any]
    aliases = CommandManager._aliases  # type: Dict[str, Any]
    choices = gen_commands_keys(commands)
    choices |= set(aliases.keys())

    raw_message = session.event.raw_message.split()
    # 假设该消息为命令，取第一个字段
    query_cmd = raw_message[0]
    cmd, confidence = process.extractOne(query_cmd, choices, scorer=fuzz.WRatio)
    logger.debug(f"query_cmd: {query_cmd}")
    logger.debug(f"fuzz cmd, confidence: {cmd} {confidence}")
    if confidence - 66 > 0:
        raw_message[0] = cmd
        await session.send(f"我猜你说的是 {cmd} 吧？")
        return IntentCommand(confidence, "switch", current_arg=" ".join(raw_message),)
