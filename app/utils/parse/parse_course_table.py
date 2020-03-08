"""
手动解析 教务处课表
"""
import math
import re
import time

from auth_swust import request
from bs4 import BeautifulSoup

from app.constants import API, INFO


def get_week():
    """
    :return: 返回当前周数
    """
    # 将格式字符串转换为时间戳
    start_time = int(time.mktime(INFO.semester_start_day))
    now_time = int(time.time())
    used_time = (now_time - start_time + 1) / (24 * 60 * 60 * 7)
    return math.ceil(used_time)


def get_course_api(sess: request.Session):
    """
    传入 requests 的 session
    返回一个list类型的API：
    [{
        'class_name': '综合英语4',
        'location': ['东2201'],
        'class_time': ['3@2-2'],
        'teacher_name': '蒋辉',
        'qsz': '01',
        'zzz': '16'
    }]
    """
    err_msg = ""

    res = sess.get(API.jwc_course_table, verify=False)
    course_table = _parse_course_table(res.text)
    exp_course_table = _parse_exp_course_table(sess)
    if exp_course_table:
        course_table.extend(exp_course_table)
    else:
        err_msg = "实验课更新失败"
    json = {
        "body": {
            "result": course_table,
            "week": get_week(),
            "updateTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "errMsg": err_msg,
        }
    }
    return json


def _parse_course_table(html):
    result_dict = {}
    location_dict = {}
    class_time_dict = {}
    """
    返回一个list：
    [{
        'class_name': '综合英语4',
        'location': ['东2201'],
        'class_time': ['3@2-2'],
        'teacher_name': '蒋辉',
        'qsz': '01',
        'zzz': '16'
    }]
    :param html: 网页
    :return: list
    """
    # 使用 requests 访问 教务处的课表
    course_table_soup = BeautifulSoup(html, "lxml")

    # 使用 bs 解析 课表所在的div
    course_table_div = course_table_soup.select_one("div#choosenCourseTable")

    # 循环遍历每个 tr 简单来说就是遍历每一讲
    for item in course_table_div.select("table.UICourseTable > tbody > tr"):
        # 这里用来判断哪一个 td 是星期一
        thres = 999
        # 周几
        day_of_the_week = 1
        # 第几讲
        lecture_count = 0

        # 循环遍历该 tr 中的每个 td
        # 简单来说就是 遍历 在第n讲下 该星期的每一天的课
        for i, c in enumerate(item.select("td")):
            if c.text.startswith("第"):
                # 判断属于星期的 td 开始
                thres = i + 1
                # 把当前是第几讲数字化
                lecture_count = l_dict[str(c.text[1])]

            if i < thres:
                continue

            # 判断课程是否冲突
            # if c["class"][1] == "attention":
            # is_conflict = True

            # 这里的 for 只是为了获取 星期i第j讲的课 因为可能课程冲突这个时间段有两节课
            for l in c.select("div.lecture"):
                # 课程名称
                class_name = l.find("span", class_="course").text
                # 教师名称
                teacher_name = l.find("span", class_="teacher").text

                # 上课周数
                week_str = str(l.find("span", class_="week").text)
                match_obj = re.match(r"(\d{2})-(\d{2}).*", week_str)

                # 上课地点
                class_place = l.find("span", class_="place").text

                # 把上课地点存起来 存成列表
                if not location_dict.get(class_name):
                    location_dict[class_name] = [class_place]
                else:
                    location_dict[class_name].append(class_place)

                # 拼装时间 形如3@2-2
                class_time = "{0}@{1}-{2}".format(day_of_the_week, lecture_count, 2)
                # 把上课时间存起来
                if not class_time_dict.get(class_name):
                    class_time_dict[class_name] = [class_time]
                else:
                    class_time_dict[class_name].append(class_time)

                # 结果
                result_dict[class_name] = {
                    "class_name": class_name,
                    "location": location_dict[class_name],
                    "class_time": class_time_dict[class_name],
                    "teacher_name": teacher_name,
                    "qsz": match_obj.group(1),
                    "zzz": match_obj.group(2),
                }

            day_of_the_week = day_of_the_week + 1
    return list(result_dict.values())


def _parse_exp_course_table(sess: request.Session):
    courses = []
    post_data = {
        "currYearterm": INFO.semester_name,
        "currTeachCourseCode": "%",
        "page": 1,
    }

    # 获取访问链接进行身份验证

    verify = sess.get(API.syk_verify_url, allow_redirects=True, verify=False)

    try:
        verify_raw = BeautifulSoup(verify.text, "lxml").script.string.strip()
    except Exception:
        return {}
    flag = verify_raw.find("'")
    verify_href = verify_raw[flag + 1 : -2]
    sess.get(API.syk_base_url + verify_href)

    # 解析实验课有关信息
    res = sess.get(API.syk_course_table)
    syk_info_soup = BeautifulSoup(res.text, "lxml")
    pagination = next(
        syk_info_soup.select("#content > div > script")[0].stripped_strings
    )
    # 获取总条数 每页条数   当前页数
    # 5         10        1
    all_course, page_size, _ = pagination[
        pagination.find("(") + 1 : pagination.find(")")
    ].split(",")

    # 获取总页数
    all_page_num = math.ceil(int(all_course) / int(page_size))

    # 第一页的课程已经可以 取出来了
    tbody_1 = syk_info_soup.select("#content > table > tbody")[0]

    for tr in tbody_1:
        if tr.name == "tr":
            course_info_lists = [content for content in tr.stripped_strings]
            if course_info_lists[0] != "课程名称":
                # 包含所有课程的list
                courses.append(_exp_list_to_dict(course_info_lists))

    # 每一页进行解析
    # 从第二页开始请求
    for page in range(2, all_page_num + 1):
        post_data["page"] = page
        res = sess.post(
            "http://202.115.175.177/StuExpbook/book/bookResult.jsp", data=post_data
        )
        # 提取出这个tbody
        soup = BeautifulSoup(res.text, "lxml")
        tbody = soup.select("#content > table > tbody")[0]

        for tr in tbody:
            if tr.name == "tr":
                course_info_lists = [content for content in tr.stripped_strings]
                if course_info_lists[0] != "课程名称":
                    # 包含所有课程的list
                    courses.append(_exp_list_to_dict(course_info_lists))

    return courses


def _exp_list_to_dict(x: list):
    week, day_of_week, class_time = re.match(r"(\d.*)周星期(.)(.*)节", x[2]).groups()
    start_class, end_class = re.match(r"(\d{1,2})-(\d{1,2})", class_time).groups()
    class_duration = int(end_class) - int(start_class) + 1
    lecture_count = math.ceil(int(start_class) / 2)

    table = {
        "class_name": x[1],
        "location": [x[3]],
        "class_time": [
            "{0}@{1}-{2}".format(l_dict[day_of_week], lecture_count, class_duration)
        ],
        "teacher_name": x[4],
        "qsz": week,
        "zzz": week,
    }
    return table


l_dict = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
