from django.contrib import admin
from .models import Profile, ChatRequest, Message, Rating

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname', 'lastname', 'location', 'learning_interest' , 'age' , 'gender']
    
@admin.register(ChatRequest)
class ChatRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
    list_filter = ['status']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'content' , "file_url")
    search_fields = ['text', 'sender__username', 'receiver__username']
    
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rater', 'ratee', 'score', 'comment' , "created_at")