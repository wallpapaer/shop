from django.conf.urls import url
from sp_user.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),  # 登录
    url(r'^register/$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^member/$', MemberView.as_view(), name='member'),  # 主页
    url(r'^forget/$', ForgetPassView.as_view(), name='forget'),  # 忘记密码
    url(r'^info/$', InfomationView.as_view(), name='info'),  # 个人资料
    url(r'^sendMsg/$', send_msg_phone, name="sendMsg"),  # 短信地址

]
