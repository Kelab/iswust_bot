import time


class API:
    studentInfo = "http://myo.swust.edu.cn/mht_shall/a/service/studentInfo"
    studentMark = "http://myo.swust.edu.cn/mht_shall/a/service/studentMark"
    card_data = "http://myo.swust.edu.cn/mht_shall/a/service/cardData?stuempno={}"
    jwc_course_table = "https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:courseTable"
    jwc_course_mark = "https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentProfile:courseMark"
    jwc_index = "https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:DEFAULT_EVENT"
    # 实验课的一些 信息 和 数据
    syk_base_url = "http://202.115.175.177"
    syk_verify_url = "http://202.115.175.177/swust/"
    syk_course_table = "http://202.115.175.177/StuExpbook/book/bookResult.jsp"
    auth_token_server = "http://cas.swust.edu.cn/authserver/login?service="


class INFO:
    term_start_day = time.strptime("2020-02-17", "%Y-%m-%d")
    term_name = "2019-2020-2"
