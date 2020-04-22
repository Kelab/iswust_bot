from app.libs.gino import db
from .base import Base


class User(Base, db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_card = db.Column(db.String(32))
    password = db.Column(db.String(64))
    bind_qq = db.Column(db.String(16))
    is_bind = db.Column(db.Integer, default=0)  # 0 not bind,1 bind
    cookies = db.Column(db.BLOB)

    @classmethod
    def add(cls, student_card: str, password: str, bind_qq: str, cookies: bytes):
        with db.auto_commit():
            db.session.add(
                User(
                    student_card=student_card,
                    password=password,
                    bind_qq=bind_qq,
                    is_bind=1,
                    cookies=cookies,
                )
            )
        return True

    @classmethod
    def remove(cls, bind_qq: str):
        with db.auto_commit():
            User.query.filter_by(bind_qq=bind_qq).update({"is_bind": 0})
        return True
