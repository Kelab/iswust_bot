import json
from collections import defaultdict
from typing import Optional

from quart import abort, request
from quart.views import MethodView

from app.services.subscribe.wrapper import SubWrapper, judge_sub
from app.utils.api import check_args, false_ret, to_token, true_ret
from app.utils.bot import qq2event

from . import api


class SubsAPI(MethodView):
    async def get(self):
        query: dict = request.args
        qq: Optional[str] = query.get("qq")
        token: Optional[str] = query.get("token")

        _, msg = check_args(qq=qq, token=token)
        if not _:
            return false_ret(msg=msg)

        if to_token(qq) != token:
            abort(403)

        user_subs = await SubWrapper.get_user_sub(qq2event(qq))  # type: ignore
        available_subs = SubWrapper.get_subs()
        result = defaultdict(dict)
        for k, v in available_subs.items():
            result[k]["name"] = v
            if user_subs.get(k):
                result[k]["enable"] = True
            else:
                result[k]["enable"] = False
        return true_ret(data=result)

    async def post(self):
        query: dict = request.args
        qq: Optional[str] = query.get("qq")
        token: Optional[str] = query.get("token")

        data = await request.get_data()

        _, msg = check_args(qq=qq, token=token)
        if not _:
            return false_ret(msg=msg)

        if to_token(qq) != token:
            abort(403)
        data = json.loads(data)

        error_key = []
        process_info = defaultdict(dict)
        for key, enable in data.items():
            SubC = judge_sub(key)
            if not SubC:
                error_key.append(key)
                continue
            if enable:
                result, p_msg = await SubC.add_sub(qq2event(qq), key)  # type: ignore
            else:
                result, p_msg = await SubC.del_sub(qq2event(qq), key)  # type: ignore
            process_info[key]["result"] = result
            process_info[key]["msg"] = p_msg
        if error_key:
            return false_ret(data=error_key, msg="error keys")
        return true_ret(data=process_info)


api.add_url_rule("/subs", view_func=SubsAPI.as_view("subs"))
