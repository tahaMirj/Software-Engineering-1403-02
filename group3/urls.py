from django.urls import path
from . import views


app_name = 'group3'
urlpatterns = [
    path('', views.home, name='group3'),
    path('login/', views.teacher_login, name='login'),  # /group3/login/
    path('signup/', views.teacher_signup, name='signup'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
]
