from django.urls import path, include
from . import views


app_name = 'group2'
urlpatterns = [
  path("chat/", include('group2_chat.urls')),
  path('', views.home, name='group2'),
] 
