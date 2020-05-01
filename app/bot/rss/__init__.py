from loguru import logger
from app.models.subcribe import SubUser
from nonebot import CommandSession, CommandGroup

rss_cg = CommandGroup("rss", only_to_me=True)


@rss_cg.command("add", only_to_me=True)
async def add(session: CommandSession):
    url = session.get("url", prompt="请输入你要订阅的地址：")

    await session.send(url)
    try:
        if await SubUser.get_sub(session.event, url):
            await session.send("已订阅~")
            return
        title, items = await SubUser.add_sub(session.event, url)
        if title:
            await session.send(title)
            await session.send(items)
            await session.send("订阅成功~")
            return
    except Exception as e:
        logger.exception(e)
        await session.send("订阅失败，请稍后重试。")


@add.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.rstrip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state["url"] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause("链接不能为空呢，请重新输入")

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
