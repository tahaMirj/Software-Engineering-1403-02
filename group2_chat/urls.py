from django.urls import path, include

from . import views

app_name = 'group2_chat'
urlpatterns = [
    path("<str:other_username>/", views.chat, name="chat"),
    path("", views.index, name="index"),
]