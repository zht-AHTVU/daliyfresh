from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^user/', include('user.urls')),# , namespace='user'
    url(r'^order/',include('order.urls')),
    url(r'^cart/',include('cart.urls')),
    url(r'^',include('goods.urls',namespace='goods')),
]
