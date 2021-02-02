from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter

from codertheory.shiritori import routing as shiritori_routing

__all__ = (
    "router",
    "application"
)

router = URLRouter(
    shiritori_routing.websocket_urlpatterns
)

application = AuthMiddlewareStack(router)
