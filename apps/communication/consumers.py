import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from apps.account.models import UserBase
from django.template.loader import render_to_string



class OnlineUserConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("users", self.channel_name)

        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, True)
            await self.send_status()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("users", self.channel_name)

        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, False)
            await self.send_status()

    async def send_status(self):
        users = UserBase.objects.all()
        html_users = render_to_string('communication/chat_platform.html', {'user': users})
        await self.channel_layer.group_send(
            'users',
            {
                "type": "user_update",
                "event": "Change Status",
                "html_users": html_users
            }
        )

    async def user_update(self, event):
        await self.send_json(event)
        print('user_update', event)

    @database_sync_to_async
    def update_user_status(self, user, status):
        return UserBase.objects.filter(id=user.pk).update(is_online=status)