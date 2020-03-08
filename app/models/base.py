import datetime

from app.libs.gino import db


class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
