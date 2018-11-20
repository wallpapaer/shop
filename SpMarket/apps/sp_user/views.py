from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginView(View):
    #登录
    def get(self,request):
        return render(request,'sp_user/login.html')

    def post(self,request):
        pass


class RegisterView(View):
    # 注册
    def get(self, request):
        pass

    def post(self, request):
        pass


class ForgetPassView(View):
    # 忘记密码
    def get(self, request):
        pass

    def post(self, request):
        pass

class MemberView(View):
    # 个人中心
    def get(self, request):
        return render(request,'sp_user/member.html')

    def post(self, request):
        pass

class InfomationView(View):
    # 个人资料
    def get(self, request):
        pass

    def post(self, request):
        pass