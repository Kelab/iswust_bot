from app.libs.gino import db
from .base import Base


class Information(Base, db.Model):
    __tablename__ = "information"

    coid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    content = db.Column(db.BLOB)
