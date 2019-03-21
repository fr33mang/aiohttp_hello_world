import os


APP_SECRET = os.environ.get('APP_SECRET', 'secret')
# time in seconds
JWT_ACCESS_TOKEN_EXP = 60*10
JWT_REFRESH_TOKEN_EXP = 60*60*24*30


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

DB_CONN_STRING = os.environ.get('DB_CONN_STRING',
                                'postgresql://postgres@localhost/postgres')
