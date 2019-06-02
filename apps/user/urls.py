from django.conf.urls import url
from apps.user.views import RegisterView,ActiveView,LoginView,UserInfoView,\
    UserOrderView,UserAddrView,UserCartView,LogoutView

app_name = 'user'
urlpatterns = [
    url(r'^register$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<token>.*)',ActiveView.as_view(),name='active'),
    url(r'^login$', LoginView.as_view(),name='login'),
    url(r'^info$', UserInfoView.as_view(), name='info'),
    url(r'^order$', UserOrderView.as_view(), name='order'),
    url(r'^addr$', UserAddrView.as_view(), name='addr'),
    url(r'^cart$', UserCartView.as_view(), name='cart'),
    url(r'^logout$',LogoutView.as_view(),name='logout'),
]