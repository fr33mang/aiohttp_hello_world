from aiohttp import web
from aiohttp_session import get_session

# from models import User


def login_required(fn):
    async def wrapped(request, *args, **kwargs):
        app = request.app
        router = app.router

        session = await get_session(request)

        if 'user_id' not in session:
            return web.HTTPFound(router['google_auth'].url_for())

        user_id = session['user_id']

        # user = await User.query.where(User.id == user_id).gino.first()

        app['user'] = user_id
        return await fn(request, *args, **kwargs)

    return wrapped
