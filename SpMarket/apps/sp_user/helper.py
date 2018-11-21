import hashlib
from django.conf import settings
from django.shortcuts import redirect

from sp_user.models import Users


def set_password(password):
    # 加密方法
    # 新的加密字符串
    new_password = "{}{}".format(password, settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode('utf-8'))
    return h.hexdigest()

def check_phone_pwd(phone, pwd):
    # 验证用户名和密码 返回用户信息
    return Users.objects.filter(phone=phone, password=set_password(pwd)).first()

# 装饰器 验证用户是否登陆
def check_is_login(old_func):
    # 新的方法 request 参数 里面有session
    def new_func_verify(request, *args, **kwargs):
        if request.session.get("ID") is None:
            # 没有登陆 跳转到登陆页面
            return redirect(settings.URL_LOGIN)
        else:
            # 已经登陆
            return old_func(request, *args, **kwargs)
    # 返回新函数
    return new_func_verify