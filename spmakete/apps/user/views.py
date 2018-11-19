import hashlib

from django.shortcuts import render, redirect


# Create your views here.
from apps.user.models import Users


def index(request):
    return render(request, 'user/member.html')


def login(request):
    #接受
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
    #处理
        try:
            user = Users.objects.get(username=username)
        except Users.MultipleObjectsReturned:
            return redirect("user:用户登录")
        except Users.DoesNotExist:
            return redirect("user:用户登录")
        h = hashlib.md5(password.encode("utf-8"))
        password = h.hexdigest()
        if password != user.password:
            return redirect("user:用户登录")
        request.session['ID'] = user.pk
        request.session['username'] = user.username
        return redirect("user:用户首页")
    else:
        return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/reg.html')
