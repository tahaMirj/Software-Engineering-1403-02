from django.urls import path
from . import views


app_name = 'group3'
urlpatterns = [
    path('', views.home, name='group3'),
    path('teacher/', views.teacher_landing, name='teacher_landing'),
    path('login/', views.teacher_login, name='login'),  # /group3/login/
    path('signup/', views.teacher_signup, name='signup'),
    path('logout/', views.teacher_logout, name='logout'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('timeslot/create/', views.create_timeslot, name='create_timeslot'),
    path('timeslot/edit/<int:slot_id>/', views.edit_timeslot, name='edit_timeslot'),
]
