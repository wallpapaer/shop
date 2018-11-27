from django.shortcuts import render

# Create your views here.
from django.views import View


class GlAddressView(View):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'sp_order/gladdress.html')

class AddressView(View):
    def post(self,request):
        return render(request,'sp_order/address.html')
    def get(self,request):
        return render(request,'sp_order/address.html')