import nonebot
from nonebot import on_command, CommandSession

from rapidfuzz import fuzz


def get_description(p):
    try:
        desc = f" ({p.module.__plugin_short_description__})"
    except Exception:
        desc = ""
    return p.name + desc


@on_command("man", aliases=["使用帮助", "帮助", "使用方法", "help"], only_to_me=False)
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            "我现在支持的功能有：\n" + "\n".join(get_description(p) for p in plugins)
        )
        await session.send("具体各功能帮助请查看：https://bot.artin.li/guide/")
        session.finish(
            '输入 "帮助+空格+功能名" 查看各功能使用指南以及命令。\n' + '如："帮助 绑定教务处"，不需要加上括号及括号内内容。'
        )

    found = False

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if fuzz.partial_ratio(p.name.lower(), arg) > 0.6:
            found = True
            session.finish(p.usage)

    if not found:
        session.finish(f"暂时没有 {arg} 这个功能呢")
