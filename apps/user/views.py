from .models import User
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
import re


# Create your views here.


# Create your views here.
def register(request):
    return render(request,'register.html')

def register_handle(request):
    '''进行注册处理'''
    # 1.接收信息
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    # 2.校验
    if not all([username, password, email]):
        return render(request,'register.html',{'errmsg':'数据不完整'})
    #校验邮箱
    if not re.match (r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请同意协议'})


    # 3.业务处理:用户注册
    # user = User()
    # user.username = username
    # user.password = password
    # user.email = email
    # user.save()
    user = User.objects.create_user(username=username,email=email,password=password)

    # create_user(username,email,password)  #创建用户，加入到数据库

    # 4.返回应答
    return redirect(reverse('goods:index'))