from django.urls import path
from . import views

app_name = 'group4'
urlpatterns = [
    # Main page
    path('', views.home, name='group4'),

    # Practice/Quiz modes
    path('practice/', views.practice_selection, name='practice_selection'),
    path('quiz', views.quiz_selection, name='quiz_selection'),

    # Reading search and detail views
    path('practice/readings/', views.reading_list_practice, name='reading_list_practice'),
    path('practice/readings/<int:reading_id>/', views.practice_mode, name='practice_mode'),
    path('quiz/readings/', views.reading_list_quiz, name='reading_list_quiz'),
    path('quiz/readings/<int:reading_id>/', views.quiz_mode, name='quiz_mode'),
    
    
    # Audio API endpoints
    path('api/readings/<int:reading_id>/generate/', views.generate_audio, name='generate_audio'),
] 