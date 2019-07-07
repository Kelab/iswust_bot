import copy
import os
import time
import imgkit
from jinja2 import Environment, FileSystemLoader


class CourseTable:
    def __init__(self):
        self._today_course_table = []
        self._today_course_table_cache = {}

    def gen_today_course_table_json(self, today, now_week_json):
        raw = now_week_json
        res = raw['body']['result']
        week = raw['body']['week']
        for x in res:
            # section_all = len(x['sksj'].split(','))
            section_all = len(x['class_time'])
            temp = section_all
            while section_all:
                if int(x['class_time'][temp - section_all][0]) == today:
                    # ensure is now week
                    if week >= int(x['qsz']) and week <= int(x['zzz']):
                        self._today_course_table_cache['class_name'] = x[
                            'class_name']
                        self._today_course_table_cache['location'] = x[
                            'location'][temp - section_all]
                        self._today_course_table_cache['teacher_name'] = x[
                            'teacher_name']
                        self._today_course_table_cache['class_time'] = x[
                            'class_time'][temp - section_all][2:]
                        self._today_course_table.append(
                            copy.deepcopy(self._today_course_table_cache))
                        self._today_course_table_cache.clear()
                section_all -= 1
        return self._today_course_table


class GenImg:
    def __init__(self, jinja2_path=None, pic_path=None):
        self.pic_path = pic_path
        if pic_path is None:
            self.pic_path = os.path.dirname(__file__)
        self._init_jinja2_env(jinja2_path)

    @staticmethod
    def tip(strs):
        after = strs.split('-')
        start = int(after[0])
        last = int(after[1])
        if start == 1 and last == 2:
            return "上午第一讲"
        if start == 1 and last == 4:
            return "上午一到二讲"
        if start == 2 and last == 2:
            return "上午第二讲"
        if start == 3 and last == 2:
            return "下午第一讲"
        if start == 3 and last == 4:
            return "下午一到二讲"
        if start == 4 and last == 2:
            return "下午第二讲"
        if start == 5 and last == 2:
            return "晚上第一讲"
        if start == 6 and last == 2:
            return "晚上第二讲"
        if start == 5 and last == 4:
            return "晚上一到二讲"

    @staticmethod
    def show_time():
        '''
        生成当天时间
        :return:
        '''
        ts = time.localtime(time.time())
        year, mon, day, wday = (ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_wday)
        return str(year) + "-" + str(mon) + "-" + str(day) + "(星期" + str(
            wday + 1) + ")"

    def _init_jinja2_env(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "template")
        env = Environment(loader=FileSystemLoader(path))

        env.globals.update(len=len, tip=GenImg.tip, show_time=GenImg.show_time)
        self._template = env.get_template('template.html')

    def render_day(self, today_course_table, filename):
        options = {
            'width': 750,
            'encoding': 'UTF-8',
        }
        imgkit.from_string(self._template.render(day_list=today_course_table),
                           os.path.join(self.pic_path, filename),
                           options=options)
