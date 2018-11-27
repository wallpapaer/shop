from django.contrib import admin

# Register your models here.
from sp_goods.models import *

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(GoodsSPU)
admin.site.register(GoodsSKU)
admin.site.register(Gallery)
admin.site.register(Banner)
admin.site.register(Activity)
admin.site.register(ActivityZone)
admin.site.register(ActivityZoneGoods)


