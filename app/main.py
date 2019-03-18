import asyncio
import base64
from cryptography import fernet

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import conf
from views import get_users, get_user, post_user
from authorization.views import google_auth, google_auth_sucess
from postgres.db import db


async def init_db():
    await db.set_bind(conf.DB_CONN_STRING)
    await db.gino.create_all()
asyncio.get_event_loop().run_until_complete(init_db())


app = web.Application()
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key, max_age=3600))

app.router.add_get('/users', get_users, name='index')
app.router.add_get('/users/{user_id}', get_user, name='user')
app.router.add_post('/users', post_user, name='post_user')

app.router.add_get('/auth/google', google_auth, name='google_auth')

app.router.add_get('/auth/google/sucess', google_auth_sucess,
                   name='google_auth_sucess')

web.run_app(app, port=5000, host='localhost')
