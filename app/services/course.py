from . import BaseService
from app.aio.requests import AsyncResponse


class CourseService(BaseService):
    _api_name = "/course"

    @classmethod
    async def deposit_ics(cls, qq: str) -> AsyncResponse:
        r: AsyncResponse = await cls._get("/depositIcs", qq)
        return r

    @classmethod
    async def get_course(cls, qq: str, **kwargs) -> AsyncResponse:
        """获取课表

        :param qq: 需要获取课表的 qq 号
        :type qq: str
        :return: 返回的 AsyncResponse 对象
        :rtype: AsyncResponse
        """
        r: AsyncResponse = await cls._get("/getCourse", qq, **kwargs)
        return r
