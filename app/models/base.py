from datetime import datetime
from sqlalchemy import Column

from app.libs.gino import db


class Base(db.Model):
    __abstract__ = True
    create_at = Column(db.DateTime, default=datetime.now)
    update_at = Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
