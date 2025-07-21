from django.urls import path
from . import views

app_name = 'group6'

urlpatterns = [
  path('', views.home, name='group6'),
  path('signup/', views.group6_signup, name='signup'), 
  path('login/', views.group6_login, name='login'),   
  path('logout/', views.group6_logout, name='logout'), 

] 