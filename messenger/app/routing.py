from django.urls import re_path
from app import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/index/$', consumers.IndexConsumer.as_asgi()),
]
