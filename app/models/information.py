from . import db


class Information(db.Model):
    __tablename__ = "information"

    coid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    content = db.Column(db.TEXT)
