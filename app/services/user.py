from . import BaseService


class UserService(BaseService):
    api_name = "/user"

    @classmethod
    async def unbind(cls, qq):
        raise NotImplementedError()
