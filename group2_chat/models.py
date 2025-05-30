from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def clean(self):
        # Check if there are exactly 2 participants
        if self.pk and self.participants.count() != 2:
            raise ValidationError("A chat must have exactly 2 participants.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        participants = list(self.participants.all())
        if len(participants) == 2:
            return f"Chat between {participants[0].username} and {participants[1].username}"
        return f"Chat {self.id}"

    @classmethod
    def get_or_create_direct_chat(cls, user1, user2):
        # Get existing chat between these users
        chats = cls.objects.filter(participants=user1).filter(participants=user2)
        if chats.exists():
            return chats.first()
        
        # Create new chat if none exists
        chat = cls.objects.create()
        chat.participants.add(user1, user2)
        return chat


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def clean(self):
        # Ensure sender is a participant in the chat
        if not self.chat.participants.filter(id=self.sender.id).exists():
            raise ValidationError("Message sender must be a participant in the chat.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}..." 