"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import config.ws_routes
from supportal.utils.middlewares import JWTMiddleware


os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="config.settings")

application = ProtocolTypeRouter(
    application_mapping={
        "http": get_asgi_application(),
        "websocket": JWTMiddleware(
            inner=URLRouter(routes=config.ws_routes.url_patterns)
        ),
    }
)
