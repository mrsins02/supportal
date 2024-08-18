import jwt
from channels.middleware import BaseMiddleware
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from jwt.exceptions import InvalidSignatureError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        UntypedToken(token)
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        user_id = decoded_data.get("user_id")
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist, InvalidSignatureError) as e:
        return str(e)


class JWTMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # get the -token- from query params
        query_string = scope.get('query_string', b'').decode()
        token = None
        if query_string:
            token = dict([part.split('=') for part in query_string.split('&')]).get(
                'token')

        if token:
            res = await get_user_from_token(token)
            if isinstance(res, str):
                scope['error'] = res
                scope['user'] = AnonymousUser()
            else:
                scope['user'] = res
        else:
            scope["error"] = "you must login first"
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
