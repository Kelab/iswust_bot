from typing import Optional
from quart import abort, request
from quart.views import MethodView

from app.services.subscribe.school_notice import get_rss_list
from app.services.subscribe.score import get_score_subscribes
from app.services.subscribe.wrapper import get_subs, handle_message, handle_rm

from . import api
from app.utils.api import check_args, false_ret, to_token, true_ret
from app.utils.bot import qq2event


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

        subs = await get_subs(qq2event(int(qq)))  # type: ignore
        return true_ret(data=subs)

    def post(self):
        ...


api.add_url_rule("/subs", view_func=SubsAPI.as_view("subs"))
