from iswust.db import db


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(64))
    qq = db.Column(db.Integer)
    usrObj = db.Column(db.TEXT)
