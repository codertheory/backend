from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from codertheory.shiritori import routing as shiritori_routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            shiritori_routing.websocket_urlpatterns
        )
    )
})
