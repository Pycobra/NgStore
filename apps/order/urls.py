from django.urls import path
from . import views
#from . import utilities

app_name="order_"
urlpatterns = [
    path('dashboard/<slug:user_name>/<slug:unique_id>/', views.user_orders, name="user_orders"),
    path('vendor/<slug:store_name>/<slug:unique_id>/', views.vendor_orders, name="vendor_orders"),
]
