from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from urllib.parse import quote
from .models import Chat

@login_required
def index(request):
    # Get all chats where the current user is a participant
    user_chats = Chat.objects.filter(participants=request.user).prefetch_related('participants')
    
    # Create a list of chat partners with their last message
    chat_partners = []
    for chat in user_chats:
        # Get the other participant (not the current user)
        other_user = chat.participants.exclude(id=request.user.id).first()
        if other_user:
            # Get the last message in this chat
            last_message = chat.messages.order_by('-timestamp').first()
            chat_partners.append({
                'username': other_user.username,
                'last_message': last_message.text if last_message else "No messages yet",
                'last_message_time': last_message.timestamp if last_message else None,
            })
    
    # Sort by last message time, newest first
    chat_partners.sort(key=lambda x: x['last_message_time'] or chat.created_at, reverse=True)
    
    return render(request, "index.html", {
        "chat_partners": chat_partners,
        "user": request.user
    })


@login_required
def chat(request, other_username):
    # Check if user is trying to chat with themselves
    if request.user.username == other_username:
        messages.error(request, "You cannot start a chat with yourself.")
        return redirect('/group2/chat')
    
    # Check if other user exists
    try:
        other_user = User.objects.get(username=other_username)
    except User.DoesNotExist:
        messages.error(request, f"The user '{other_username}' does not exist.")
        return redirect('/group2/chat')

    # Get or create chat room for these users
    chat = Chat.get_or_create_direct_chat(request.user, other_user)
    
    # Get previous messages
    previous_messages = chat.messages.order_by('timestamp').select_related('sender')
    
    return render(request, "chat.html", {
        "other_username": other_username,
        "previous_messages": previous_messages,
        "user": request.user
    })