from apps.user.models import User
from django.shortcuts import render,redirect
from django.urls import reverse
import re
from django.views.generic import View
from django.http import HttpResponse

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
        # 4.返回应答
        return redirect(reverse('goods:index'))  # 反向代理
# def register(request):
#     if request.method == 'GET':  #GET方式显示注册页面
#         return render(request,'register.html')
#     else:

