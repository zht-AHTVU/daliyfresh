from apps.user.models import User,Address
from django.shortcuts import render,redirect
from django.urls import reverse
import re
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from django.http import HttpResponse
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
from django.db import models


class RegisterView(View):
    '''注册'''
    def get(self, request):
        # GET请求方式的话，就显示注册界面的UI
        return render(request, 'register.html')

    def post(self,request):
        # 1.接收信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email', '')
        allow = request.POST.get('allow')
        # 2.校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已注册，请更换'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = 0
        user.save()
        # 发送激活邮件，包含激活链接/user/active/id
        # 激活链接中包含用户身份信息，并且要加密,生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()
        send_register_active_email.delay(email,username,token)
        # 4.返回应答
        return render(request, 'register.html', {'errmsg': '注册成功，请前往注册邮箱激活您的账号！'})

class ActiveView(View):
    def get(self,request,token):
        #进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as err:
            # 激活链接已过期
            return HttpResponse(err)


class LoginView(View):
    def get(self,request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '请输入用户名、密码！'})
        user = authenticate(username=username,password=password)
        if user is not None:
            #记录用户登录状态
            login(request,user)
            # 获取登录后跳转地址，默认跳转到首页
            next_url = request.GET.get('next',reverse('goods:index'))
            response = redirect(next_url)
            if remember == 'on':
                response.set_cookie('username',username,max_age=7*34*3600)
            else:
                response.delete_cookie('username')
            return response
        else:
            return render(request, 'login.html', {'errmsg': '账号未激活或用户名、密码错误！'})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('goods:index'))

class UserInfoView(LoginRequiredMixin, View):
    def get(self,request):
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request,'user_center_info.html',{'page':'info','address':address})

class UserOrderView(LoginRequiredMixin, View):
    def get(self,request):
        # 获取用户的订单信息
        return render(request,'user_center_order.html',{'page':'order'})



class UserAddrView(LoginRequiredMixin, View):
    def get(self,request):
        # 获取用户的默认收获地址
        user = request.user
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        # add_obj = Address.objects
        address =Address.objects.get_default_address(user)
        return render(request,'user_center_addr.html',{'page':'addr','address':address})
    def post(self,request):
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code','')
        tel = request.POST.get('tel')
        # 校验数据
        if not all([receiver,addr,tel]):
            return render(request,'user_center_addr.html',{'errmsg':'数据不完整'})
        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8|9][0-9]{9}$',tel):
            return render(request, 'user_center_addr.html', {'errmsg': '请输入正确的手机号'})
        # 存储数据
        # 如果已有默认收获地址，不作默认，没有的话作为默认地址
        address = Address.objects.get_default_address(request.user)
        if address:
            is_default = False
        else:
            is_default = True
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=tel,
                               is_default=is_default)

        return redirect(reverse('user:addr'))

class UserCartView(LoginRequiredMixin, View):
    def get(self,request):
        return render(request,'cart.html')


