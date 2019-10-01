import regex as re

from nonebot import IntentCommand, NLPSession, on_natural_language

from utils.qqai.aaiasr import rec_silk

record_re = re.compile(r'\[CQ:record,file=([A-Z0-9]{32}\.silk)\]')


@on_natural_language()
async def _(session: NLPSession):
    msg: str = session.ctx.get('raw_message')

    if msg.startswith('[CQ:record,'):
        # [CQ:record,file=8970935D1A480B008970935D1A480B00.silk]
        match = record_re.search(msg)
        if match:
            filename = match.group(1)
            text = await rec_silk(filename)
            session.send(text)
            return IntentCommand(75.0, text)

    if not ('课' in msg):
        return IntentCommand(90.0, 'hitokoto')
