from django.urls import path
from . import views


app_name = 'group3'
urlpatterns = [
    path('', views.home, name='group3'),
    path('teacher/', views.teacher_landing, name='teacher_landing'),
    path('login/', views.teacher_login, name='teacher_login'),  # /group3/login/
    path('signup/', views.teacher_signup, name='teacher_signup'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('student-login/', views.student_login, name='student_login'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('timeslot/create/', views.create_timeslot, name='create_timeslot'),
    path('timeslot/edit/<int:slot_id>/', views.edit_timeslot, name='edit_timeslot'),
    path('teacher/profile/edit/', views.edit_profile, name='edit_profile'),
    path('student/', views.student_landing, name='student_landing'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('student/teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('student/book/<int:slot_id>/', views.book_timeslot, name='book_timeslot'),
    path('student/sessions/', views.student_sessions, name='student_sessions'),
    path('student/teachers/<int:teacher_id>/review/', views.add_review, name='add_review'),
    path('reviews/', views.view_reviews, name='view_reviews'),
]
