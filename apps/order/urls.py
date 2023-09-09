from django.urls import path
from . import views
#from . import utilities

app_name="order_"
urlpatterns = [
    path('dashboard/<slug:user_name>/<slug:unique_id>/', views.user_orders, name="user_orders"),
    path('vendor/<slug:store_name>/<slug:unique_id>/', views.vendor_orders, name="vendor_orders"),
    #path("addresses/", views.view_address, name="addresses"),
    #path("add_address/", views.add_address, name="add_address"),
    #path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    #path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    #path("addresses/set_default/", views.set_default, name="set_default"),
]
