from . import BaseService


class CourseService(BaseService):
    api_name = "/course"

    @classmethod
    async def deposit_ics(cls, qq: str):
        r = await cls.get("/depositIcs", qq)
        return r

    @classmethod
    async def get_course(cls, qq: str, params: dict = {}, **kwargs):
        """获取课表

        :param qq: 需要获取课表的 qq 号
        :type qq: str
        :return: 返回的 AsyncResponse 对象
        :rtype: AsyncResponse
        """
        r = await cls.get("/getCourse", qq, params, **kwargs)
        return r
