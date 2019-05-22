from django.conf.urls import url
from apps.cart import views


urlpatterns = [
    url(r'^index$',views.index),
]