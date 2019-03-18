from aiohttp import web

from aiohttp_session import new_session
from aioauth_client import GoogleClient

import conf


google_client = GoogleClient(
    client_id=conf.GOOGLE_CLIENT_ID,
    client_secret=conf.GOOGLE_CLIENT_SECRET,
    redirect_uri='http://localhost:5000/auth/google/sucess'
)
scope = 'https://www.googleapis.com/auth/userinfo.email'
google_authorize_url = google_client.get_authorize_url(scope=scope)


async def google_auth(request):
    raise web.HTTPFound(google_authorize_url)


async def google_auth_sucess(request):
    code = request.rel_url.query.get('code')

    if not code:
        return web.HTTPBadRequest()

    access_token, _ = await google_client.get_access_token(code)

    google = GoogleClient(
        client_id=conf.GOOGLE_CLIENT_ID,
        client_secret=conf.GOOGLE_CLIENT_SECRET,
        access_token=access_token,
    )

    resp = await google.request('GET', google.user_info_url)

    session = await new_session(request)
    session['user_id'] = resp['email']

    return web.HTTPFound('/users')
