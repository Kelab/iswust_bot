from . import BaseService
from app.aio.requests import AsyncResponse


class UserService(BaseService):
    api_name = "/user"

    @classmethod
    async def unbind(cls, qq) -> AsyncResponse:
        r: AsyncResponse = await cls.get("/unbind", qq)
        return r
