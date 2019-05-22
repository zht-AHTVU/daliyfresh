from django.conf.urls import url
from apps.user import views


urlpatterns = [
    url(r'^index$',views.index),
]