from django.urls import path

from codertheory.polls import consumers

__all__ = (
    "websocket_urlpatterns",
)

websocket_urlpatterns = [
    path("ws/polls/<slug:poll>", consumers.PollConsumer.as_asgi())
]
