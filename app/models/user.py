from sqlalchemy import Column
from app.libs.gino import db
from .base import Base


class User(Base, db.Model):
    """用户表 Model
    """

    __tablename__ = "user"

    qq = Column(db.String(16), primary_key=True)
    student_id = Column(db.String(32))
    password = Column(db.String(64), nullable=False)
    name = Column(db.String(64))
    class_ = Column("class", db.String(16))
    cookies = Column(db.LargeBinary)

    @classmethod
    async def add(
        cls, *, qq: str, student_id: str, password: str, user_info: dict, cookies
    ):
        user = User(
            student_id=student_id,
            qq=qq,
            password=password,
            cookies=cookies,
            class_=user_info.get("class"),
        )
        await user.create()
        return user

    @classmethod
    async def unbind(cls, qq: str):
        user = await User.query.where(User.qq == qq).gino.first()
        await user.delete()
        return True
