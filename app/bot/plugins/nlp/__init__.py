import regex as re

from nonebot import IntentCommand, NLPSession, on_natural_language, get_bot

from utils.qqai.aaiasr import rec_silk
from utils.tools import post_msg

bot = get_bot()

record_re = re.compile(r'\[CQ:record,file=([A-Z0-9]{32}\.silk)\]')


@bot.on_message()
async def _(context):
    msg: str = context['raw_message']

    if msg.startswith('[CQ:record,'):
        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(msg)
        if match:
            filename = match.group(1)
            text = await rec_silk(filename)
            await bot.send(context, text)
            await post_msg(context, text)
            return

    if not ('课' in msg):
        await post_msg(context, 'hitokoto')
        return
