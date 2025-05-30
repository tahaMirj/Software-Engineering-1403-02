from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:other_username>/", views.chat, name="chat"),
]