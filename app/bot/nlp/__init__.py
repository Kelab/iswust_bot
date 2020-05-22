from typing import Any, Dict, Tuple

from loguru import logger
from nonebot import IntentCommand, NLPSession, on_natural_language
from nonebot.command import CommandManager
from rapidfuzz import fuzz, process


def gen_commands_keys(commands: Dict[Tuple, Any]):
    result = []
    for item in commands.keys():
        if len(item) == 1:
            result.append(item[0])
    return result


@on_natural_language()
async def _(session: NLPSession):
    commands = CommandManager._commands  # type: Dict[Tuple, Any]
    choices = gen_commands_keys(commands)
    aliases = CommandManager._aliases  # type: Dict[str, Any]
    choices.extend(list(aliases.keys()))
    msg = session.event.raw_message
    cmd, confidence = process.extractOne(
        session.event.raw_message, choices, scorer=fuzz.WRatio
    )
    logger.debug(f"session.event.raw_message: {msg}")
    logger.debug(f"cmd, confidence: {cmd} {confidence}")
    if confidence >= 60.0:
        # choose the intent command with highest confidence
        logger.debug(f"fuzz result: {cmd}")
        result = cmd.split(" ")
        result[0] = cmd
        result = " ".join(result)
        return IntentCommand(confidence, "switch", current_arg=result,)
