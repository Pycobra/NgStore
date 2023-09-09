from django.urls import path
from django.conf.urls import url

from . import views

app_name="vendor_"
urlpatterns = [
    path('add-category/', views.add_category, name="add_category_"),
    path('store/<slug:unique_id>/', views.vendor_store, name="vendor_store_"),
    path('vendor_admin_ajax/', views.vendor_admin_ajax, name="vendor_admin_ajax"),
    path('add-product/', views.add_product, name="add_product_"),
    path('delete-product/', views.delete_product, name="delete_product_"),
    path('follow-unfollow/', views.follow_unfollow, name="follow_unfollow"),
    path('become-vendor/', views.become_vendor, name="become_vendor_"),
    path('edit-vendor/', views.edit_vendor, name="edit_vendor_"),
    path('sell-on-NGstoreboy/', views.sell, name="sell"),
    path('<slug:unique_id>/', views.vendor_admin, name="vendor_admin_"),
    #url(r'^<slug:vendor_id>/(?P<hierarchy>.+)/$', views.vendor_admin2, name='vendor_admin2_'),
    path('site_vendors/', views.vendors_list, name="site_vendors_"),
    path('edit-product/<int:id>/', views.edit_product, name="edit_product_"),
    path('suscribe-to-vendor/<int:vendor_id>/', views.suscribe_to_vendor, name="suscribe_to_vendor_"),
    path('<slug:unique_id>/', views.suscribe_package, name="suscribe_package_"),
    path('', views.vendors_list, name="vendors_list_"),
    path('<slug:vendor_id>/<slug:category_slug>/', views.vendor_admin2, name='vendor_admin2_'),
]