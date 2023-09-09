from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url
from . import views


app_name="cart_"
urlpatterns = [
    path("cart_update_address/", views.cart_update_address, name="cart_update_address"),
    path('', views.cart_detail, name="cart_detail"),
    path('', views.shopping_cart, name="shopping_cart_"),
    path('success/', views.success, name="success_"),
    path("all/<str:rep>/", views.complete_payment, name="complete_payment2"),
]