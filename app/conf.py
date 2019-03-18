import os


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

DB_CONN_STRING = os.environ.get('DB_CONN_STRING',
                                'postgresql://postgres@localhost/postgres')
