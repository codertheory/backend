from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ChannelNameRouter

from codertheory.polls import routing as polls_routing
from codertheory.shiritori import routing as shiritori_routing

__all__ = (
    "router",
    "application"
)

from codertheory.shiritori.consumers import BackGroundTimerConsumer

urls = [
    *polls_routing.websocket_urlpatterns,
    *shiritori_routing.websocket_urlpatterns
]

router = URLRouter(urls)

channels = ChannelNameRouter({
    "timer": BackGroundTimerConsumer.as_asgi()
})

application = AuthMiddlewareStack(router)
