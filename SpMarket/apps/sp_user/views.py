import random
import re
import uuid

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django_redis import get_redis_connection

from sp_user.forms import RegisterModelForm, LoginForm, UserChangeModelForm
from sp_user.helper import set_password, check_phone_pwd, check_is_login, send_sms, login
from sp_user.models import Users


@check_is_login
def foo(request):
    pass


# 登录
class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'sp_user/login.html', {'form': form})

    def post(self, request):
        data = request.POST
        form = LoginForm(data)
        if form.is_valid():
            # 和数据库验证
            data = form.cleaned_data
            phone = data.get('phone')
            password = data.get('password')
            user = check_phone_pwd(phone, password)
            if user:
                # 验证成功后,将用户登录标识符保存到session
                # request.session.clear()
                request.session['ID'] = user.pk
                request.session['phone'] = user.phone
                request.session.set_expiry(0)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                else:
                    # 跳转到用户中心
                    return redirect("sp_user:member")
            else:
                context = {
                    'errors': form.errors,
                }
                return render(request, 'sp_user/login.html', context)


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, 'sp_user/reg.html')

    def post(self, request):
        # 接受数据
        data = request.POST
        form = RegisterModelForm(data)
        if form.is_valid():
            # 处理数据
            data = form.cleaned_data
            password = data.get('password2')
            password = set_password(password)
            Users.objects.create(phone=data.get('phone'), password=password)
            # 响应
            return redirect('sp_user:login')
        else:
            context = {
                'errors': form.errors
            }
            return render(request, 'sp_user/reg.html', context)

    # 忘记密码


class ForgetPassView(View):
    def get(self, request):
        return render(request, 'sp_user/forgetpassword.html')

    def post(self, request):
        pass


@check_is_login
def center(request):
    # 如果session中没有用户ID,说明没有登录，就跳转到登录页面
    # if request.session.get("ID") is None:
    #     return redirect("/user/login/")
    return render(request, "sp_user/member.html")

    # 个人中心


class MemberView(View):

    def get(self, request):
        context = {
            'phone': request.session.get('phone')
        }
        return render(request, 'sp_user/member.html', context)

    def post(self, request):
        pass

    # 视图类的装饰
    @method_decorator(check_is_login)
    def dispatch(self, request, *args, **kwargs):
        return super(MemberView, self).dispatch(request, *args, **kwargs)

    # 个人资料


class InfomationView(View):

    def get(self, request):
        id = request.session.get('ID')
        user = Users.objects.filter(pk=id).values().first()
        user_change_form = UserChangeModelForm(user)
        return render(request, 'sp_user/infor.html', {"form": user_change_form})

    def post(self, request):
        # 获取需要更改的数据
        user = Users.objects.filter(pk=request.session.get('ID')).first()
        data = request.POST
        user_change_form = UserChangeModelForm(data, instance=user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect(reverse('sp_user:member'))
        else:
            return render(request, 'sp_user/infor.html', {"form": user_change_form})

    @method_decorator(check_is_login)
    def dispatch(self, request, *args, **kwargs):
        return super(InfomationView, self).dispatch(request, *args, **kwargs)


# 发送短信的视图函数
def send_msg_phone(request):
    if request.method == 'POST':
        # 接受手机号码
        phone = request.POST.get('phone', '')  # ''指以免为NONE时报错
        # 验证手机是否错误
        phone_re = re.compile('^1[3-9]\d{9}$')
        rs = re.search(phone_re, phone)
        if not rs:
            return JsonResponse({'err': 1, 'errmsg': '手机输入的格式不正确'})
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])  # 下划线可以作为无用的变量

        # 保存随机码到数据库中
        r = get_redis_connection('default')
        r.set(phone, random_code)
        r.expire(phone, 60)
        # 发送短信
        print(random_code)

        # 使用阿里发送短信
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"云通信\"}" %random_code
        print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))

        return JsonResponse({'err': 0})
    else:
        return JsonResponse({'err': 1, 'errmsg': '请求方式错误!'})



