import asyncio

from aiohttp import web
from views import get_users, get_user, post_user
from postgres.db import db


async def init_db():
    await db.set_bind('postgresql://postgres@localhost/postgres')
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(init_db())

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)

app.router.add_get('/users', get_users, name='index')
app.router.add_get('/users/{user_id}', get_user, name='user')
app.router.add_post('/users', post_user, name='post_user')
web.run_app(app)
