import nonebot
from nonebot import on_command, CommandSession


@on_command('usage', aliases=['使用帮助', '帮助', '使用方法'])
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send('我现在支持的功能有：\n' + '\n'.join(p.name for p in plugins))
        await session.send('输入 "帮助+空格+功能名" 查看具体功能\n' + '如："帮助 绑定教务处"')
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
