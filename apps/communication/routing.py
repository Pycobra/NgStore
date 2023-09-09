from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import OnlineUserConsumer

"""application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path("new-user /", OnlineUserConsumer),
            ]
        )
    )
})"""
from django.urls import re_path
websocket_urlpatterns = [
    re_path(r'ws/message/(?P<user_or_vendor_unique_id>\w+)/$', OnlineUserConsumer.as_asgi()),
]
