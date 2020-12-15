from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from codertheory.shiritori.consumers import LobbyConsumer, GameConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/shiritori/lobby", LobbyConsumer),
            path("ws/shiritori/<uuid:game>", GameConsumer)
        ])
    )
})
