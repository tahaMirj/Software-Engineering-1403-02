from django.urls import path
from . import views


app_name = 'group1' 
urlpatterns = [
  path('', views.home, name='group1'),
  path('grammar-quiz/', views.grammar_quiz_question, name='grammar_quiz_question'),
  path('vocabulary-quiz/', views.vocabulary_quiz_question, name='vocabulary_quiz_question'),
  path('image-quiz/', views.image_quiz_question, name='image_quiz_question'),
  path('writing-quiz/', views.writing_quiz_question, name='writing_quiz_question'),
  path('sentence-building-quiz/', views.sentence_building_question, name='sentence_building_question'),
  path('listening-quiz/', views.listening_quiz_question, name='listening_quiz_question'),
] 
