from django.conf.urls import url
from apps.order import views


urlpatterns = [
    url(r'^index$',views.index),
]