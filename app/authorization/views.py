from http import HTTPStatus
from json import JSONDecodeError
from aiohttp import web

import jwt
from aioauth_client import GoogleClient

from conf import APP_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from authorization.utils import experied_at
from authorization.models import RefreshToken
from models import User


google_client = GoogleClient(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
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
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        access_token=access_token,
    )

    resp = await google.request('GET', google.user_info_url)

    user = await User.query.where(User.google_id == resp['id']).gino.first()
    if not user:
        user = await User.create(
            nickname=resp['email'].split('@')[0],
            email=resp['email'],
            google_id=resp['id']
        )

    payload = {
        'exp': experied_at(),
        'user_id': user.id
    }
    access_token = jwt.encode(payload, APP_SECRET).decode('utf-8')

    payload['exp'] = experied_at(access_token=False)
    refresh_token = jwt.encode(payload, APP_SECRET).decode('utf-8')

    await RefreshToken.create(token=refresh_token)

    return web.json_response({
        'access_token': access_token,
        'refresh_token': refresh_token,
    })


async def refresh_token(request):
    # app = request.app
    # router = app.router

    try:
        data = await request.json()
    except JSONDecodeError:
        return web.json_response(
            data={
                'message': 'No json in request body'
            },
            status=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    token = data.get('refresh_token')
    if not token:
        return web.json_response(
            data={
                'message': 'No refresh token in json'
            },
            status=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    filters = [RefreshToken.token == token]
    db_token = await RefreshToken.query.where(*filters).gino.first()
    if not db_token:
        return web.json_response(
            data={
                'message': 'Refresh token is revoked or illegal'
            },
            status=HTTPStatus.UNAUTHORIZED
        )

    await db_token.delete()
    try:
        refresh_token = jwt.decode(token, APP_SECRET)
    except jwt.ExpiredSignatureError:
        return web.json_response(
            data={
                'message': 'Refresh token is expired, please relogin'
            },
            status=HTTPStatus.UNAUTHORIZED
        )

    user_id = refresh_token['user_id']
    user = await User.query.where(User.id == user_id).gino.first()

    payload = {
        'exp': experied_at(),
        'user_id': user.id
    }
    access_token = jwt.encode(payload, APP_SECRET).decode('utf-8')

    payload['exp'] = experied_at(access_token=False)
    refresh_token = jwt.encode(payload, APP_SECRET).decode('utf-8')

    await RefreshToken.create(token=refresh_token)

    return web.json_response({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
