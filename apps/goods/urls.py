from django.conf.urls import url
from apps.goods import views


urlpatterns = [
    url(r'',views.index),
    url(r'^index$',views.index),
]