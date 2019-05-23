from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^tinymce/',include('tinymce.urls')),  #富文本编辑器
    url(r'^user/',include('apps.user.urls',namespace='user')),
    url(r'^order/',include('apps.order.urls',namespace='order')),
    url(r'^cart/',include('apps.cart.urls',namespace='cart')),
    url(r'^',include('apps.goods.urls',namespace='goods')),
]
