from typing import Dict, List, Set

from loguru import logger
from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot.command import Command, CommandManager
from nonebot.permission import check_permission
from nonebot.typing import CommandName_T
from rapidfuzz import fuzz, process


def gen_commands_keys(commands: Dict[CommandName_T, Command]):
    result_set: Set[str] = set()
    for item in commands.keys():
        if len(item) == 1:
            result_set.add(item[0])
    return result_set


@on_natural_language()
async def _(session: NLPSession):
    raw_message: List[str] = session.event["raw_message"].split()
    # 假设该消息为命令，取第一个字段
    query_cmd = raw_message[0]

    fuzz_cmd = None
    confidence = None
    # 检查 commands
    commands_dct = CommandManager._commands
    choices = gen_commands_keys(commands_dct)
    # 模糊匹配命令与 commands
    result = process.extractOne(query_cmd, choices, scorer=fuzz.WRatio)
    if result:
        cmd_name, confidence = result
        _cmd = (cmd_name,)
        if commands_dct.get(_cmd) is not None:
            if check_permission(
                session.bot, session.event, commands_dct[_cmd].permission
            ):
                fuzz_cmd = cmd_name

    # 检查 commands 没有匹配到命令
    if fuzz_cmd is None:
        # 检查 aliases
        aliases_dct = CommandManager._aliases  # type: Dict[str, Command]
        choices = set(aliases_dct.keys())
        # 模糊匹配命令与 aliases
        result = process.extractOne(query_cmd, choices, scorer=fuzz.WRatio)
        if result:
            alias, confidence = result
            if check_permission(
                session.bot, session.event, aliases_dct[alias].permission
            ):
                fuzz_cmd = alias

    if fuzz_cmd is not None and confidence is not None:
        logger.debug(f"query_cmd: {query_cmd}")
        logger.debug(f"fuzz cmd, confidence: {fuzz_cmd} {confidence}")
        if confidence - 66 > 0:
            raw_message[0] = fuzz_cmd
            return IntentCommand(
                confidence, "switch", current_arg=" ".join(raw_message),
            )
