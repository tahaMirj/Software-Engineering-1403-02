from django.urls import path

from .views import *
from . import views


urlpatterns = [
    path('', views.home, name='home'), 
    path('profile/', views.profile, name='profile'),
    path('signup/',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path('logout/',LogoutPage,name='logout'),
]

