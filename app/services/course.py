from . import BaseService
from loguru import logger
from app.models.course import Course


class CourseService(BaseService):
    api_name = "/course"

    @classmethod
    async def deposit_ics(cls, qq: str):
        return await cls.get("/depositIcs", qq)

    @classmethod
    async def get_course(cls, qq: str, params: dict = {}, **kwargs):
        """获取课表

        :param qq: 需要获取课表的 qq 号
        :type qq: str
        """
        logger.info(f"qq {qq} 正在请求课表!")
        course = await Course.get_course_schedule(qq)
        return course
