from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection

from sp_goods.models import Banner, GoodsSKU, Activity, ActivityZone, Category


# 首页
def index(request):
    banners = Banner.objects.filter(is_delete=False).order_by('order')  # 轮播
    activetys = Activity.objects.filter(is_delete=False)  # 活动
    activetys_zone = ActivityZone.objects.filter(is_on_sale=True, is_delete=False).order_by('order')
    context = {
        'banners': banners,
        'activetys': activetys,
        'activetys_zone': activetys_zone
    }
    return render(request, 'sp_goods/index.html', context)



# 商城
def category(request, cate_id, order):
    try:
        cate_id = int(cate_id)
        order = int(order)
    except:
        return redirect('sp_goods:首页')
    # 关于商品分类
    category = Category.objects.filter(is_delete=False)

    # 关于物品
    if cate_id == 0:  # 默认查询第一个
        catefirst = category.first()
        cate_id = catefirst.pk

    if order == 0:
        goodsSku = GoodsSKU.objects.filter(is_delete=False, is_on_sale=True, category_id=cate_id)
    elif order == 1:
        goodsSku = GoodsSKU.objects.filter(is_on_sale=True, is_delete=False, category_id=cate_id).order_by('-sale_num')
    elif order == 2:
        goodsSku = GoodsSKU.objects.filter(is_on_sale=True, is_delete=False, category_id=cate_id).order_by('-price')
    elif order == 3:
        goodsSku = GoodsSKU.objects.filter(is_on_sale=True, is_delete=False, category_id=cate_id).order_by('price')
    elif order == 4:
        goodsSku = GoodsSKU.objects.filter(is_on_sale=True, is_delete=False, category_id=cate_id).order_by('-create_time')
    else:
        redirect('sp_goods:首页')
    #购物车商品的数量的显示
    cart_count = 0
    if request.session.get('ID'):
        user_id = request.session.get('ID')
        r =get_redis_connection('default')
        cart_key = 'cart_key_{}'.format(user_id)
        cart_values = r.hvals(cart_key)
        # print(cart_values)
        for v in cart_values:
            # print(int(v))
            cart_count += int(v)

    context = {
        'category': category,
        'goodsSku': goodsSku,
        'cate_id': cate_id,
        'order': order,
        'cart_count': cart_count,
    }

    return render(request, "sp_goods/category.html", context)


# 详情
def detail(request, id):
    try:
        goodsSku = GoodsSKU.objects.get(pk=id, is_on_sale=True)
    except GoodsSKU.DoesNotExist:
        return redirect("sp_goods:首页")

    context = {
        "goodsSku": goodsSku
    }
    return render(request, 'sp_goods/detail.html', context)
