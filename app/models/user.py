from sqlalchemy import Column
from app.libs.gino import db
from .base import Base


class User(Base, db.Model):
    """用户表 Model
    """

    __tablename__ = "user"

    qq = Column(db.String(16), primary_key=True)
    student_id = Column(
        db.String(32),
        db.ForeignKey("student.student_id", onupdate="CASCADE", ondelete="SET NULL"),
    )
    is_bind = Column(db.Boolean, default=False)

    @classmethod
    async def add(cls, student_id: str, qq: str):
        user = User(student_id=student_id, qq=qq, is_bind=True,)
        await user.create()
        return user

    @classmethod
    async def unbind(cls, qq: str):
        user = await User.query.where(User.qq == qq).gino.first()
        await user.update(is_bind=False).apply()
        return True

    @classmethod
    async def get_user_by_qq(cls, qq: str):
        user = await User.query.where(User.qq == qq).gino.first()
        return user
