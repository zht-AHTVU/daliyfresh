from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
# import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','daliyfresh.settings')
# django.setup()


# 使用celery
app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/8')
#定义任务函数
@app.task
def send_register_active_email(to_email,username,token):

    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 收件人列表
    html_message = '<h1>%s,欢迎您成为天天生鲜注册会员！</h1>请点击下面的链接激活您的账户：<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' %(username,token,token)
    send_mail(subject, message, sender, receiver, html_message=html_message)  # 发送邮件
