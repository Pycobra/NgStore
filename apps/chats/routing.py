from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from .consumers import ChatConsumer #OnlineUserConsumer

"""application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path("new-user /", OnlineUserConsumer),
            ]
        )
    )
})"""
websocket_urlpatterns = [
    #re_path(r'ws/message/(?P<user_or_vendor_unique_id>\w+)/$', OnlineUserConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi())
]
