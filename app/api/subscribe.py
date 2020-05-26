from typing import Optional

from quart import abort, request
from quart.views import MethodView

from app.services.subscribe.wrapper import SubWrapper
from app.utils.api import check_args, false_ret, to_token, true_ret
from app.utils.bot import qq2event

from . import api


class SubsAPI(MethodView):
    async def get(self):
        query: dict = request.args
        print("query: ", query)
        qq: Optional[str] = query.get("qq")
        token: Optional[str] = query.get("token")

        result, msg = check_args(qq=qq, token=token)
        if not result:
            return false_ret(msg=msg)

        if to_token(qq) != token:
            abort(403)

        user_subs = await SubWrapper.get_user_sub(qq2event(qq))  # type: ignore
        available_subs = SubWrapper.get_subs()

        return true_ret(data=available_subs)

    def post(self):
        ...


api.add_url_rule("/subs", view_func=SubsAPI.as_view("subs"))
