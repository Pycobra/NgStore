"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core_')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/home.png'))),
    path('vendors/', include('apps.vendor.urls', namespace='vendor_')),
    path('account/', include('apps.account.urls', namespace='account_')),
    path('cart/', include('apps.cart.urls', namespace='cart_')),
    path('chat/', include('apps.chats.urls', namespace='chat_')),
    path('order/', include('apps.order.urls', namespace='order_')),
    path('checkout/', include('apps.checkout.urls', namespace='checkout_')),
    path('message/', include('apps.communication.urls', namespace='message_')),
    path('', include('apps.product.urls', namespace='product_')),
    # path('', include('apps.order.urls', namespace='order_')),
    path('__debug__/', include(debug_toolbar.urls)),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
