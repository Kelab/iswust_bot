from typing import Optional
from collections import defaultdict
from quart import abort, request
from quart.views import MethodView

from app.services.subscribe.wrapper import SubWrapper
from app.utils.api import check_args, false_ret, to_token, true_ret
from app.utils.bot import qq2event

from . import api
import json


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

    async def put(self):
        query: dict = json.loads(await request.get_data())
        qq: Optional[str] = query.get("qq")
        token: Optional[str] = query.get("token")
        _, msg = check_args(qq=qq, token=token)
        if not _:
            return false_ret(msg=msg)

        if to_token(qq) != token:
            abort(403)


api.add_url_rule("/subs", view_func=SubsAPI.as_view("subs"))
