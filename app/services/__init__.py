from app.constants.config import api_url
from app.utils.tools import bot_hash


class BaseService:
    base_url = api_url
    api_name = ""

    @classmethod
    def url(cls):
        # http://xxxx/api/v1 + /user
        return cls.base_url + cls.api_name

    @classmethod
    async def get(cls, method: str, qq: str, params: dict = {}, **kwargs: dict):
        raise NotImplementedError()
        if not method.startswith("/"):
            raise SyntaxError("method 参数有误")
