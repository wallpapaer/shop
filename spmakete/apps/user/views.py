from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'user/member.html')


def login(request):
    return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/reg.html')