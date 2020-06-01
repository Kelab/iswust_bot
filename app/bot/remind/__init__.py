"""
修改自：https://github.com/nonebot/nonebot-alarm
原作者： yanyongyu
原作者GitHub： https://github.com/yanyongyu
"""

from nonebot import get_bot

__plugin_name__ = "⏰ 提醒"
__plugin_short_description__ = "[原 push]命令：remind"
__plugin_usage__ = r"""
帮助链接：https://bot.artin.li/guide/remind.html

新建提醒输入：
    - remind
    - 提醒
    - 添加提醒
    - 新增提醒
    - 新建提醒

查看提醒可以输入：
    - remind.show
    - 查看提醒
    - 我的提醒
    - 提醒列表

删除提醒：
    - remind.rm
    - 取消提醒
    - 停止提醒
    - 关闭提醒
    - 删除提醒
""".strip()

bot = get_bot()
nickname = getattr(bot.config, "NICKNAME", "我")

EXPR_COULD_NOT = (f"哎鸭，{nickname}没有时光机，这个时间没办法提醒你。", f"你这是要穿越吗？这个时间{nickname}没办法提醒你。")

EXPR_OK = (
    "遵命！我会在{time}叫你{action}！\n",
    "好！我会在{time}提醒你{action}！\n",
    "没问题！我一定会在{time}通知你{action}。\n",
    "好鸭~ 我会准时在{time}提醒你{action}。\n",
    "嗯嗯！我会在{time}准时叫你{action}哒\n",
    "好哦！我会在{time}准时叫你{action}~\n",
)

EXPR_REMIND = (
    "提醒通知：\n提醒时间到啦！该{action}了！",
    "提醒通知：\n你设置的提醒时间已经到了~ 赶快{action}！",
    "提醒通知：\n你应该没有忘记{action}吧？",
    "提醒通知：\n你定下的提醒时间已经到啦！快{action}吧！",
)

from . import commands, nlp  # noqa: F401
