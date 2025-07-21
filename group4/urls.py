from django.urls import path
from . import views

app_name = 'group4'
urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('readings/', views.reading_list, name='reading_list'),
    path('readings/<int:reading_id>/', views.reading_detail, name='reading_detail'),
    
    # Practice/Quiz modes
    path('readings/<int:reading_id>/practice/', views.practice_mode, name='practice_mode'),
    path('readings/<int:reading_id>/quiz/', views.quiz_mode, name='quiz_mode'),
    
    # Audio API endpoints
    path('api/readings/<int:reading_id>/audio/', views.get_audio, name='get_audio'),
    path('api/readings/<int:reading_id>/audio/generate/', views.generate_audio, name='generate_audio'),
    
    # Subtitle and timing API endpoints
    path('api/readings/<int:reading_id>/subtitles/', views.get_subtitles, name='get_subtitles'),
    path('api/readings/<int:reading_id>/sentences/<int:sentence_id>/timestamp/', views.get_sentence_timestamp, name='sentence_timestamp'),
    
    # Exercise and progress API endpoints
    path('api/readings/<int:reading_id>/exercises/', views.reading_exercises, name='reading_exercises'),
    path('api/readings/<int:reading_id>/exercises/<int:exercise_id>/submit/', views.submit_exercise, name='submit_exercise'),
    path('api/user/progress/', views.user_progress, name='user_progress'),
    path('api/user/level/adjust/', views.adjust_user_level, name='adjust_user_level'),
] 