import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing as chat_routing
from user import routing as user_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenTherapy.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns +
            user_routing.websocket_urlpatterns
        )
    ),
})
