from django.conf.urls import url

from sp_order.views import GlAddressView, AddressView

urlpatterns = [
    url('^gladd$',GlAddressView.as_view(),name='选择收货地址'),
    url('^add$',AddressView.as_view(),name='添加收货地址'),
]