from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^user/',include('apps.user.urls')),
    url(r'^',include('apps.goods.urls')),
    url(r'^order/',include('apps.order.urls')),
    url(r'^cart/',include('apps.cart.urls')),
]
