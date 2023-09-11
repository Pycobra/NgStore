


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
"""from apps.communication import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NgStore.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack( 
        URLRouter(
            routing.websocket_urlpatterns,
        )
    ),
})"""

from apps.chats import routing

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NgStore.settings")

application = ProtocolTypeRouter({
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns,
        )
    ),
})
