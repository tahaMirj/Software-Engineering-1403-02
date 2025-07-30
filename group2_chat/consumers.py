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
        self.chat_room_group_name = f"chat_{self.chat.id}"
        self.chat_lobby_group_name = f"lobby_{self.other_user.id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_group_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(    
            self.chat_lobby_group_name, self.channel_name
        )

        self.accept()
        if self.chat.blocked:
            self.send_blocked_state()

        # Send all messages in the chat to the connected user
        messages = Message.objects.filter(chat=self.chat).order_by('timestamp')
        for message in messages:
            self.send(text_data=json.dumps({
                "type": "chat_message",
                "message": message.text,
                "sender_username": message.sender.username,
                "timestamp": message.timestamp.isoformat(),
                "message_id": message.id
            }))

        # Mark all messages in this chat as seen
        seen_count = Message.objects.filter(
            chat=self.chat,
            sender=self.other_user,
            seen=False
        ).update(seen=True)

        # Send success connection message
        self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": f"Connected to chat with {self.other_username}"
        }))

        # If any messages were marked as seen, notify the other user
        if seen_count > 0:
            # Notify other user that messages have been seen
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_group_name,
                {
                    "type": "messages_seen",
                    "user": self.user.username
                }
            )

        # Check if any messages from current user were already seen
        seen_messages_exist = Message.objects.filter(
            chat=self.chat,
            sender=self.user,
            seen=True
        ).exists()

        if seen_messages_exist:
            # Send seen status for user's own messages
            self.send(text_data=json.dumps({
                "type": "messages_seen",
                "user": self.other_username
            }))

    def disconnect(self, close_code):
        if hasattr(self, 'chat_room_group_name'):
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.chat_room_group_name, self.channel_name
            )
        if hasattr(self, 'chat_lobby_group_name'):
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.chat_lobby_group_name, self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("action") == "refresh_state":
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_group_name,
                {
                    "type": "refresh_state",
                    # "blocked_by": self.user.username
                }
            )
            return
        
        # Reject sending if blocked
        self.chat.refresh_from_db()
        if self.chat.blocked:
            return

        
        message_text = text_data_json["message"]

        # Create message instance
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            text=message_text
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender_username": self.user.username,
                "timestamp": message.timestamp.isoformat(),
                "message_id": message.id,
            }
        )

    def chat_message(self, event):
        # If the other user is the sender and we're connected, mark the message as seen
        if event['sender_username'] != self.user.username:
            Message.objects.filter(
                chat=self.chat,
                sender__username=event['sender_username'],
                id=event['message_id']
            ).update(seen=True)

            # Send seen notification back
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_group_name,
                {
                    "type": "messages_seen",
                    "user": self.user.username
                }
            )

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
            "message_id": event["message_id"]
        }))

    def messages_seen(self, event):
        # Send seen status to WebSocket
        self.send(text_data=json.dumps({
            "type": "messages_seen",
            "user": event["user"]
        }))


    def refresh_state(self, event):
        self.send_blocked_state()

    def send_blocked_state(self):
        self.chat.refresh_from_db()
        self.send(text_data=json.dumps({
            "type": "update_state",
            "blocked": self.chat.blocked,
            "blocked_by": self.chat.blocked_by.username if self.chat.blocked else None
        }))