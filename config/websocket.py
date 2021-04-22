from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ChannelNameRouter
from django.urls import path

from codertheory.shiritori import routing as shiritori_routing
from codertheory.shiritori.consumers import BackGroundTimerConsumer
from config.api import GraphQLConsumer

__all__ = (
    "router",
    "channels",
    "application"
)

urls = [
    *shiritori_routing.websocket_urlpatterns,
    path("graphql", GraphQLConsumer.as_asgi())
]

router = URLRouter(urls)

channels = ChannelNameRouter({
    "timer": BackGroundTimerConsumer.as_asgi()
})

application = AuthMiddlewareStack(router)
