import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from apps.account.models import UserBase
from django.template.loader import render_to_string

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data = json.dumps({'message':message}))
