from django.urls import path
from . import views

app_name="message_"
urlpatterns = [
    path("send-fleet-message", views.send_fleet_message, name="send_fleet_message"),
    path("<slug:user_unique_id>/<slug:logged_in_user_unique_id>", views.get_message, name="chat_platform2"),
    path("<slug:user_unique_id>/<slug:logged_in_user_unique_id>/", views.send_message, name="send_msg"),
    path("<slug:user_or_vendor_unique_id>", views.messages_history, name="messages_history"),
    path('', views.make_comment, name="make_comment"),
]
