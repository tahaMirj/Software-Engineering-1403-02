from django.urls import path, include
from . import views


app_name = 'group2'
urlpatterns = [
  path('user/<str:username>/', views.profile_view_or_edit, name='profile_page'),
  path("find_partners/", views.find_partners, name="find_partner"),
  path("chat/", include('group2_chat.urls')),
  path('api/v1/', include('group2.api.v1.urls')),
  path('', views.home, name='group2'),
] 
