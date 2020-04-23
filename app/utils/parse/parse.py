import json


def parse_grade(grade_json, info_json, type):
    grade_msg = ""
    info = json.loads(info_json["body"]["result"])
    gpa_msg = (
        "总成绩绩点：" + str(info["gpa"]["all"]) + "\n必修课绩点：" + str(info["gpa"]["required"])
    )
    credit_msg = (
        "总成绩学分："
        + str(info["credit"]["all"])
        + "\n必修课学分："
        + str(info["credit"]["required"])
    )

    if type == "1":
        term_dict = {}
        grade = json.loads(grade_json["body"]["result"])
        for x in grade:
            term = str(x["term"])
            if not term_dict.get(term):
                term_dict[term] = 1
                grade_msg = grade_msg + "\n" + term[:-1] + "-" + term[-1] + "学期成绩如下：\n"
            grade_msg = (
                grade_msg
                + str(x["catalog"])
                + "-"
                + x["course"]
                + "-"
                + x["scroll"]
                + "\n"
            )
    else:
        grade = json.loads(grade_json["body"]["result"])
        grade_msg = "当前学期成绩如下：\n"
        for x in grade:
            # TODO 自动判断当前学期
            if x["term"] == "181":
                grade_msg = (
                    grade_msg
                    + str(x["catalog"])
                    + "-"
                    + x["course"]
                    + "-"
                    + x["scroll"]
                    + "\n"
                )
    return grade_msg, credit_msg, gpa_msg
