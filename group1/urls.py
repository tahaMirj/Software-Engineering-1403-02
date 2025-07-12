from django.urls import path
from . import views


app_name = 'group1' 
urlpatterns = [
  path('', views.home, name='group1'),
  path('grammar-quiz/', views.grammar_quiz_question, name='grammar_quiz_question'),
] 
