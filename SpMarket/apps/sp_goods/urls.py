from django.conf.urls import url

from sp_goods.views import index , category , detail

urlpatterns = [
    url(r'^$', index, name="首页"),
    url(r'^category/(?P<cate_id>\d+)/(?P<order>\d)$', category, name="商城"),
    url(r'^(?P<id>\d+)$', detail, name="详情"),
]