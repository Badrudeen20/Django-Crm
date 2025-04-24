from django.urls import re_path
from .consumers import MyConsumer,ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/somepath/$', MyConsumer.as_asgi()),
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]