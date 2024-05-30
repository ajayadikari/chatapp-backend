from django.urls import path
from .consumers import MyAsyncConsumer


websocket_urlpatterns = [
    path('ws/sc/<str:username>', MyAsyncConsumer.as_asgi()),
]