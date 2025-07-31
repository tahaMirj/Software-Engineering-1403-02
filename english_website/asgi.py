"""
ASGI config for english_website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'english_website.settings')
django.setup()

django_asgi_app = get_asgi_application()

from group2_chat.routing import websocket_urlpatterns as g2_websocket_urlpatterns
from group5.routing import websocket_urlpatterns as g5_websocket_urlpatterns
websocket_urlpatterns = g2_websocket_urlpatterns + g5_websocket_urlpatterns
# This wraps the default django ASGI app for more functionalities like support for ws protocol
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
