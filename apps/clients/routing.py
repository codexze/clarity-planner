from django.urls import re_path
from .consumers import ClientConsumer

websocket_urlpatterns = [
    re_path(r'ws/client/$', ClientConsumer.as_asgi()),
]
