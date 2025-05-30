from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__username',)
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'short_text', 'timestamp')
    list_filter = ('timestamp', 'sender')
    search_fields = ('text', 'sender__username')
    raw_id_fields = ('chat', 'sender')
    readonly_fields = ('timestamp',)
    
    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Message' 