import hashlib

from django.shortcuts import render, redirect


# Create your views here.
from apps.sp_user.models import Users


def index(request):
    return render(request, 'sp_user/member.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
        h = hashlib.md5(password.encode('utf-8'))
        Users.objects.create(username=username,password=password)
        return render(request,'sp_user/login.html')
    else:
        return render(request,'sp_user/reg.html')

def login(request):
    #接受
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
    #处理
        try:
            user = Users.objects.get(username=username)
        except Users.MultipleObjectsReturned:
            return redirect("sp_user:登录界面")
        except Users.DoesNotExist:
            return redirect("sp_user:登录界面")
        h = hashlib.md5(password.encode("utf-8"))
        # password = h.hexdigest()
        if password != user.password:
            return redirect("sp_user:登录界面")
        request.session['ID'] = user.pk
        request.session['username'] = user.username
        return redirect("sp_user:用户主页")
    else:
        return render(request,'sp_user/login.html')

def step(request):
    return render(request,'sp_user/step.html')

def about(request):
    return render(request,'sp_user/about.html')