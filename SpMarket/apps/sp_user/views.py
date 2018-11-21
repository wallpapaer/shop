from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from sp_user.forms import RegisterModelForm, LoginForm, UserChangeModelForm
from sp_user.helper import set_password, check_phone_pwd, check_is_login
from sp_user.models import Users


@check_is_login
def foo(request):
    pass

#登录
class LoginView(View):

    def get(self,request):
        form = LoginForm()
        return render(request,'sp_user/login.html',{'form':form})

    def post(self,request):
        data = request.POST
        form = LoginForm(data)
        if form.is_valid():
            #和数据库验证
            data = form.cleaned_data
            phone = data.get('phone')
            password = data.get('password')
            user = check_phone_pwd(phone,password)
            if user:
                #验证成功后,将用户登录标识符保存到session
                # request.session.clear()
                request.session['ID'] = user.pk
                request.session['phone'] = user.phone
                request.session.set_expiry(24 * 3600)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                else:
                    # 跳转到用户中心
                    return redirect(reverse("sp_user:member"))
            else:
                context = {
                    'errors': form.errors,
                }
                return render(request, 'sp_user/login.html', context)


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request,'sp_user/reg.html')

    def post(self, request):
        #接受数据
        data = request.POST
        form = RegisterModelForm(data)
        if form.is_valid():
            #处理数据
            data = form.cleaned_data
            password = data.get('password2')
            password = set_password(password)
            Users.objects.create(phone=data.get('phone'),password=password)
            #响应
            return redirect('sp_user:login')
        else:
            context = {
                'errors':form.errors
            }
            return render(request,'sp_user/reg.html',context)


    # 忘记密码
class ForgetPassView(View):
    def get(self, request):
        return render(request,'sp_user/forgetpassword.html')

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
            'phone':request.session.get('phone')
        }
        return render(request,'sp_user/member.html',context)

    def post(self, request):
        pass

    #视图类的装饰
    @method_decorator(check_is_login)
    def dispatch(self, request, *args, **kwargs):
        return super(MemberView,self).dispatch(request, *args, **kwargs)


    # 个人资料
class InfomationView(View):

    def get(self, request):
        id = request.session.get('ID')
        user = Users.objects.filter(pk=id).values().first()
        user_change_form = UserChangeModelForm(user)
        return render(request,'sp_user/infor.html',{"form": user_change_form})

    def post(self, request):
        #获取需要更改的数据
        user = Users.objects.filter(pk=request.session.get('ID')).first()
        data = request.POST
        user_change_form = UserChangeModelForm(data,instance=user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect(reverse('sp_user:member'))
        else:
            return render(request,'sp_user/infor.html',{"form": user_change_form})

    @method_decorator(check_is_login)
    def dispatch(self, request, *args, **kwargs):
        return super(InfomationView,self).dispatch(request, *args, **kwargs)