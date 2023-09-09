from django.urls import path
from . import views
from django.conf.urls import url
from .templatetags import searching


app_name="product_"
urlpatterns = [
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    path('search/', views.search, name="search_"),
    path('filter/', views.filter_page, name="filter_page"),
    path('search-for', views.search_single, name="search_single"),
    path('search-brand/', views.search_brand, name="search_brand"),
    path('check-category/', views.parent_child_check, name="parent_child_check"),
    path('<slug:category_slugz>/<slug:product_slugz>/', views.product_detail, name="product_detail_"),
    path('', views.product_detail2, name="product_detail2_"),
    path('<slug:category_slug>/', views.category_list, name="category_list_"),
    path('', views.vendor_category, name="vendor_category"),
    path('add-product/', views.add_product, name="add_product_"),
    path('add-category/', views.add_category, name="add_category_"),
    path('likes_add_and_remove/<int:id>', views.likes_add_and_remove, name="likes_add_and_remove"),
    path("likes/remove_from_likes/", views.remove_from_likes, name="remove_from_likes"),
    #path('product/', views.product_entry, name="product_"),
    path('', views.make_comment, name="make_comment"),
]
