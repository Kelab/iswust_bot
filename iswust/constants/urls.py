class API():
    studentInfo = 'http://my.swust.edu.cn/mht_shall/a/service/studentInfo'
    studentMark = 'http://my.swust.edu.cn/mht_shall/a/service/studentMark'
    jwc_course_table = "https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:courseTable"
    # 实验课的一些 信息 和 数据
    syk_base_url = "http://202.115.175.177"
    syk_verify_url = "http://202.115.175.177/swust/"
    syk_course_table = "http://202.115.175.177/StuExpbook/book/bookResult.jsp"

    @staticmethod
    def get_some_week_class(week=0):
        url = 'http://my.swust.edu.cn/mht_shall/a/service/courseData?frontWeek=' + str(
            week)
        return url
