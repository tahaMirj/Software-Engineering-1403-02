from django.urls import path
from . import views


app_name = 'group1' 
urlpatterns = [
  path('', views.home, name='group1'),
  path('grammar-quiz/', views.grammar_quiz_question, name='grammar_quiz_question'),
  path('start-grammar-quiz/', views.start_grammar_quiz, name='start_grammar_quiz'),
  path('vocabulary-quiz/', views.vocabulary_quiz_question, name='vocabulary_quiz_question'),
  path('start-vocabulary-quiz/', views.start_vocabulary_quiz, name='start_vocabulary_quiz'),
  path('image-quiz/', views.image_quiz_question, name='image_quiz_question'),
  path('writing-quiz/', views.writing_quiz_question, name='writing_quiz_question'),
  path('sentence-building-quiz/', views.sentence_building_question, name='sentence_building_question'),
  path('listening-quiz/', views.listening_quiz_question, name='listening_quiz_question'),
  path('quiz-complete/<int:quiz_id>/', views.quiz_complete, name='quiz_complete'),
  path('reset-quiz/<int:quiz_id>/', views.reset_quiz, name='reset_quiz'),
] 
