from django.urls import path, include
from . import views


app_name = 'group2'
urlpatterns = [
    path("block/", views.BlockView.as_view(), name="block"),
    path("unblock/", views.UnblockView.as_view(), name="unblock"),
] 