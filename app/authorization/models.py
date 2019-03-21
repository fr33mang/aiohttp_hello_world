from postgres.db import db


class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    token = db.Column(db.String())
