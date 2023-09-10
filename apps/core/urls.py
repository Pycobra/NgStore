from django.urls import path
from . import views
from apps import communication

app_name="core_"
urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('contact/', views.contact, name="contact"),
    path('search/<slug:category>/', views.category_search, name="category_search"),
]
