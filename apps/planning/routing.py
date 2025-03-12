from django.urls import re_path
from .consumers import PlanningConsumer

websocket_urlpatterns = [
    re_path(r'ws/planning/$', PlanningConsumer.as_asgi()),
]
