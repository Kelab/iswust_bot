from nonebot import on_command, CommandSession
from utils.tools import bot_hash, dwz
from app.bot.constants.config import web_url
from typing import Optional, Any
from urllib.parse import urlencode

__plugin_name__ = "绑定教务处(命令：bind)"
__plugin_usage__ = r"""对我发以下关键词开始绑定：
绑定、绑定教务处、bind"""


@on_command("bind", aliases=("绑定", "绑定教务处"))
async def bind(session: CommandSession):
    await session.send(f"开始请求绑定~ 请等待")

    sender: dict[str, Any] = session.ctx.get("sender", {})
    sender_qq: Optional[str] = sender.get("user_id")
    nickname: Optional[str] = sender.get("nickname")

    if sender_qq:
        token = bot_hash(sender_qq)
        # web 登录界面地址
        query: str = urlencode({
            "qq": sender_qq,
            "nickname": nickname,
            "token": token
        })

        url_ = f"{web_url}?{query}"
        shorten_url_ = await dwz(url_)
        if shorten_url_:
            await session.finish(f"请点击链接绑定：{shorten_url_}")
        await session.finish(f"请点击链接绑定：{url_}")
