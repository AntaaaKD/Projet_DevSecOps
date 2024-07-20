# routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video-call/<str:room_name>/', consumers.VideoCallConsumer.as_asgi()),
]
