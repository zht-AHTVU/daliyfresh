from django.conf.urls import url
from apps.user import views


urlpatterns = [
    url(r'^register$',views.register),
    url(r'^register_handle$',views.register_handle),
]