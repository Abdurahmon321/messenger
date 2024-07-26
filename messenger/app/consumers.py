import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message
from datetime import datetime
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.room_name:
            await self.close()  # room_name bo'sh bo'lsa, ulanishni yopish
            return
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        sender = self.scope['user']
        chat = await sync_to_async(Chat.objects.get)(slug=self.room_name)

        # Xabarni databasega saqlash
        message = await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=sender,
            content=message_content
        )

        # Xabarni vaqti va shifrlangan xabarni olish
        timestamp = message.timestamp.isoformat()
        decrypted_message = message.decrypted_content

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': decrypted_message,
                'sender': sender.username,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': str(message),
            'sender': sender,
            'timestamp': timestamp
        }))



class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'index_updates'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def index_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
