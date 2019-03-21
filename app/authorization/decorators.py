from http import HTTPStatus
import jwt
from aiohttp import web

from conf import APP_SECRET


def jwt_required(fn):
    async def wrapped(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return web.json_response(
                data={
                    'message': 'Missing Authorization header'
                },
                status=HTTPStatus.UNAUTHORIZED
            )

        _, access_token = auth_header.split(' ')
        try:
            token = jwt.decode(access_token, APP_SECRET)
        except jwt.ExpiredSignatureError:
            return web.json_response(
                data={
                    'message': 'Token has expired, use refresh_token',
                    'refresh_endpoint': '/auth/token/refresh',
                },
                status=HTTPStatus.UNAUTHORIZED
            )

        request.user_id = token['user_id']

        return await fn(request, *args, **kwargs)

    return wrapped
