from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/g2_chat/(?P<other_username>[\w.@+-]+)/$", consumers.ChatConsumer.as_asgi()),
]