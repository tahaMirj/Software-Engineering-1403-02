import json
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import quote
from django.conf import settings
from .models import Chat, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_authenticated:
            # Get the current path from the scope
            path = self.scope["path"].decode('utf-8')
            # Accept the connection temporarily to send the redirect message
            self.accept()
            self.send(text_data=json.dumps({
                "type": "redirect",
                "url": f"{settings.LOGIN_URL}?next={quote(path)}"
            }))
            self.close()
            return

        self.user = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["other_username"]
        
        try:
            self.other_user = User.objects.get(username=self.other_username)
        except User.DoesNotExist:
            # Accept the connection temporarily to send the error message
            self.accept()
            self.send(text_data=json.dumps({
                "type": "error",
                "message": f"User '{self.other_username}' does not exist."
            }))
            self.close()
            return

        # Get or create chat room for these users
        self.chat = Chat.get_or_create_direct_chat(self.user, self.other_user)
        self.room_group_name = f"chat_{self.chat.id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        # Send success connection message
        self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": f"Connected to chat with {self.other_username}"
        }))

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        # Create message instance
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            text=message_text
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_text,
                "sender_username": self.user.username,
                "timestamp": message.timestamp.isoformat()
            }
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"]
        }))