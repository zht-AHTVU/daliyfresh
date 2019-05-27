from apps.user.models import User
from django.shortcuts import render,redirect
from django.urls import reverse
import re
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from django.http import HttpResponse
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email

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
        return render(request,'login.html')

