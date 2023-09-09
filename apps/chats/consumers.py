import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from apps.account.models import UserBase
from django.template.loader import render_to_string

"""class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        #leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receives msg from webSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # sends msg to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # receives msg from room group
    async def chat_message(self, event):
        message = event['message']

        #sends msg to webSocket
        await self.send(text_data=json.dumps({'message': message}))"""

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data = json.dumps({'message':message}))


"""class OnlineUserConsumer(AsyncJsonWebsocketConsumer):
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
        return UserBase.objects.filter(id=user.pk).update(is_online=status)"""