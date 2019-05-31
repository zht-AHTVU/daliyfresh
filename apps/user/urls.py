from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from apps.user.views import RegisterView,ActiveView,LoginView,UserInfo,UserOrder,UserAddr,UserCart

app_name = 'user'
urlpatterns = [
    url(r'^register$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<token>.*)',ActiveView.as_view(),name='active'),
    url(r'^login$', LoginView.as_view(),name='login'),
    url(r'^info$',login_required(UserInfo.as_view()),name='info'),
    url(r'^order$',login_required(UserOrder.as_view()),name='order'),
    url(r'^addr$',login_required(UserAddr.as_view()),name='addr'),
    url(r'^cart$',login_required(UserCart.as_view()),name='cart')
]