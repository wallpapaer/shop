from django.conf.urls import url
from sp_user.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),  # 登录
    url(r'^register/$', RegisterView.as_view()),  # 注册
    url(r'^member/$', MemberView.as_view()),  # 主页
    url(r'^forget/$',ForgetPassView.as_view()),#忘记密码
    url(r'^info/$',InfomationView.as_view()),#个人资料
 ]