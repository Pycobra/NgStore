from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.conf.urls import url
from . import views


app_name="chat_"
urlpatterns = [
    path("", views.index, name="chat"),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name="room")
]