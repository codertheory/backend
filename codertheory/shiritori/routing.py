from django.urls import path

from codertheory.shiritori import consumers

websocket_urlpatterns = [
    path("ws/shiritori/lobby", consumers.LobbyConsumer.as_asgi()),
    path("ws/shiritori/<uuid:game>", consumers.GameConsumer.as_asgi()),
]
