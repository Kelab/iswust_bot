from app.constants.config import api_url
from app.aio import requests
from app.aio.requests import AsyncResponse
from app.utils.tools import bot_hash


class BaseService:
    _base_url_prefix = api_url + '/api/v1'

    @classmethod
    def url(cls):
        # /api/v1 + /user
        return cls._base_url_prefix + cls._api_name

    @classmethod
    async def _get(cls, method: str, qq: str, **kwargs) -> AsyncResponse:
        if not method.startswith('/'):
            raise SyntaxError("method 参数有误")

        params: dict = kwargs.get("params", dict())
        params.update({
            "qq": qq,
            "token": bot_hash(qq),
        })
        r: AsyncResponse = await requests.get(cls.url() + method,
                                              params=params,
                                              **kwargs)
        return r
