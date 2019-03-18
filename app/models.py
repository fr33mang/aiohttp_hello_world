from postgres.db import db


class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'public'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.String(), unique=True)
