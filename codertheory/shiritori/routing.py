from django.urls import path

from codertheory.shiritori import consumers

__all__ = (
    "websocket_urlpatterns",
)

websocket_urlpatterns = [
    path("ws/shiritori/lobby", consumers.LobbyConsumer.as_asgi()),
    path("ws/shiritori/game/<slug:game>", consumers.GameConsumer.as_asgi()),
]
