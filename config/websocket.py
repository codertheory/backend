from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ChannelNameRouter
from django.urls import path

from codertheory.shiritori.consumers import BackGroundTimerConsumer
from config.api import GraphQLConsumer

__all__ = (
    "router",
    "channels",
    "application"
)

urls = [
    path("graphql", GraphQLConsumer.as_asgi())
]

router = URLRouter(urls)

channels = ChannelNameRouter({
    "timer": BackGroundTimerConsumer.as_asgi()
})

application = AuthMiddlewareStack(router)
