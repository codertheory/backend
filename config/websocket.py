from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter

from codertheory.shiritori import routing as shiritori_routing

websocket_application = AuthMiddlewareStack(
    URLRouter(
        shiritori_routing.websocket_urlpatterns
    )
)
