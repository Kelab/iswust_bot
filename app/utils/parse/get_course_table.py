import copy


class CourseTable:
    def __init__(self):
        self._today_course_table = []
        self._today_course_table_cache = {}

    def gen_today_course_table_json(self, today, now_week_json):
        raw = now_week_json
        res = raw["body"]["result"]
        week = raw["body"]["week"]
        for x in res:
            # section_all = len(x['sksj'].split(','))
            section_all = len(x["class_time"])
            temp = section_all
            while section_all:
                if int(x["class_time"][temp - section_all][0]) == today:
                    # ensure is now week
                    if week >= int(x["qsz"]) and week <= int(x["zzz"]):
                        self._today_course_table_cache["class_name"] = x["class_name"]
                        self._today_course_table_cache["location"] = x["location"][
                            temp - section_all
                        ]
                        self._today_course_table_cache["teacher_name"] = x[
                            "teacher_name"
                        ]
                        self._today_course_table_cache["class_time"] = x["class_time"][
                            temp - section_all
                        ][2:]
                        self._today_course_table.append(
                            copy.deepcopy(self._today_course_table_cache)
                        )
                        self._today_course_table_cache.clear()
                section_all -= 1
        return self._today_course_table
