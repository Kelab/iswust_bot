from app.libs.gino import db
from .base import Base


class User(Base, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_card = db.Column(db.String(32))
    password = db.Column(db.String(64), nullable=False)
    bind_qq = db.Column(db.String(16))
    is_bind = db.Column(db.Boolean, default=False)
    cookies = db.Column(db.LargeBinary)

    @classmethod
    async def add(cls, student_card: str, password: str, bind_qq: str, cookies: bytes):
        user = User(
            student_card=student_card,
            password=password,
            bind_qq=bind_qq,
            is_bind=True,
            cookies=cookies,
        )
        await user.create()
        return user

    @classmethod
    async def remove(cls, bind_qq: str):
        user = await User.query.where(User.bind_qq == bind_qq).gino.first()
        await user.update(is_bind=False).apply()
        return True
