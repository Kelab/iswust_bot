from app.services import BaseService
from app.services.user import UserService
from app.services.course import CourseService
from app.constants.config import api_url

test_api_name = "/init"


class InitTest(BaseService):
    api_name = test_api_name


class TestServices:
    def test_init(self):
        assert InitTest.url() == api_url + test_api_name

    def test_course(self):
        assert CourseService.api_name == "/course"

    def test_user(self):
        assert UserService.api_name == "/user"
