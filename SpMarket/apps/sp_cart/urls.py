from django.conf.urls import url

from sp_cart.views import AddCartView, CartShowView

urlpatterns = [
    url(r'^addCart/$', AddCartView.as_view(), name="addCart"),
    url(r'^$', CartShowView.as_view(), name="CartShow"),
]