from nonebot import (CommandSession, NLPSession, IntentCommand, on_command,
                     on_natural_language)

from log import IS_LOGGER
from time_converter import TimeNormalizer  # 引入包
from utils.tools import xor_encrypt
from iswust.constants.config import api_url
from .parse_course_schedule import week_course, parse_date, get_week, parse_course_by_date, str_number_wday_dict
from typing import List
import requests

tn = TimeNormalizer(isPreferFuture=False)

__plugin_name__ = '查询课表'
__plugin_usage__ = r"""输入 查询课表/课表"""


@on_command('course_schedule', aliases=('查询课表', '课表'))
async def course_schedule(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    r = requests.get(api_url + 'api/v1/course/getCourse',
                     params={"verifycode": xor_encrypt(sender_qq)})
    if r and r.json():
        IS_LOGGER.info('课表:' + str(r.json()))
        resp = r.json()
        if resp['code'] == 200:
            data = resp['data']
            if session.state.get('week') and session.state.get('wday'):
                week = session.state.get('week')
                wday = session.state.get('wday')
                IS_LOGGER.info("检测到时间意图：" + str(session.state))
                course = parse_course_by_date(data, week, wday)
                await session.finish(course)
            else:
                course_dict = week_course(data)
                week_course_list: List[str] = course_dict['week_course_list']
                for i in week_course_list:
                    await session.send(i)
                await session.finish("今天的课程：\n" + course_dict['today'])
        elif resp['code'] == -1:
            await session.finish("未绑定！")

    await session.finish('查询出错')


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language('课')
async def process_accu_date(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    res = tn.parse(target=session.ctx.get('raw_message'))
    IS_LOGGER.debug("时间意图分析结果:" + str(res))
    resp_type_: str = res.get('type')
    if resp_type_ != 'error':
        await session.send(f'您所说的时间是：{res.get(resp_type_)}')
        date = parse_date(res.get(resp_type_))
        wday = str(date.timetuple().tm_wday + 1)
        week = get_week(date.timestamp())
        await session.send(f"第{week}周，星期{wday}")
        IS_LOGGER.info(
            f"第{str(week)}周，星期{str_number_wday_dict.get(wday,wday)}")
        args = {
            "wday": wday,
            "week": week,
        }
        return IntentCommand(90.0, 'course_schedule', args=args)
