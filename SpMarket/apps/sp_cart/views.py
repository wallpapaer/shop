from django.shortcuts import render
# Create your views here.
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from sp_goods.models import GoodsSKU


# 增加
class AddCartView(View):
    def post(self, request):
        user_id = request.session.get('ID')  # 获取登录的ID
        if user_id is None:
            return JsonResponse({'code': 1, 'errmsg': '您还没有登录,请登录'})  # 未登录时的错误提示

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')  # 接受参数:购物车加入的当前商品ID以及数量

        try:
            sku_id = int(sku_id)
            count = int(count)  # 将接受到的字符串转换为整数
        except:
            return JsonResponse({'code': 2, 'errmsg': '参数错误'})

        try:
            gsku = GoodsSKU.objects.get(pk=sku_id)
        except:
            return JsonResponse({'code': 3, 'errmsg': '商品不存在'})  # 判断商品是否存在

        # if count <= 0:
        #     return JsonResponse({'code': 4, 'errmsg': '请输入正确的商品数量'})  # 判断商品数量

        if gsku.stock < count:
            return JsonResponse({'code': 5, 'errmsg': '该商品库存不足,请重写填写购买数量'})  # 判断库存是否足够

        # 使用redis数据库来添加商品到购物车
        r = get_redis_connection('default')

        ckey = 'cart_key_%s' % user_id

        r.hincrby(ckey, sku_id, count)  # 存储到redis中

        # 计算现在购物车中的商品的数量
        # cart_total = 0
        # vars = r.hvals(ckey)
        # if len(vars) > 0:
        #     for v in vars:
        #         cart_total += int(v)

        return JsonResponse({
            'code': 6,
            # 'cart_total': cart_total
        })

    def get(self, request):
        pass


# 显示购物车
class CartShowView(BaseVerifyView):
    def post(self, request):
        pass

    def get(self, request):
        r = get_redis_connection('default')
        cart_key = 'cart_key_{}'.format(request.session.get('ID'))
        cart_data = r.hgetall(cart_key)
        # 遍历所有购物车信息
        gskus = []
        for sku_id, count in cart_data.items():
            sku_id = int(sku_id)
            count = int(count)

            # 查询购物车商品的完整信息
            gsku = GoodsSKU.objects.get(pk=sku_id)

            # 自定义一个属性保存count
            gsku.count = count

            # 保存
            gskus.append(gsku)
        context = {
            'goodssku': gskus,
        }

        return render(request, "sp_cart/shopcart.html", context)
