import datetime

from conf import JWT_ACCESS_TOKEN_EXP, JWT_REFRESH_TOKEN_EXP


def experied_at(access_token=True):
    if access_token:
        exp_seconds = JWT_ACCESS_TOKEN_EXP
    else:
        exp_seconds = JWT_REFRESH_TOKEN_EXP

    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=exp_seconds)
    return now + delta
