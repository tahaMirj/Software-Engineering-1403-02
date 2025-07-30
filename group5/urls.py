from django.urls import path
from group5 import views

app_name = 'group5'

urlpatterns = [
    path('', views.home, name='group5'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('media/avatar/<str:filename>/', views.serve_avatar, name='serve_avatar'),
    path('media/chat_files/<str:filename>/', views.serve_file, name='serve_file'),
    path('send-request/<int:user_id>/', views.send_chat_request, name='send_chat_request'),
    path('chat-requests/', views.chat_requests_view, name='chat_requests'),
    path('chat-request/<int:request_id>/<str:action>/', views.respond_to_chat_request, name='respond_to_chat_request'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('search/', views.search_users, name='search_users'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('settings/account/', views.my_profile, name='my_profile'),
    path('chat-partners/', views.chat_partners, name='chat_partners'),
    path('rate/<str:username>/', views.rate_partner, name='rate_partner'),
    path('rating/<str:username>/', views.view_rating, name='view_rating'),
    path('settings/general/', views.general_settings, name='settings_general'),
    path('settings/billing/', views.billing_settings, name='settings_billing'),
    path('settings/notifications/', views.view_rating, name='settings_notifications'),
    path('upload/', views.upload_file, name='upload_file'),

]
