from postgres.db import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    google_id = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    nickname = db.Column(db.String(), unique=True)
