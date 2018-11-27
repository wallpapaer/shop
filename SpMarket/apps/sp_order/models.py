from django.db import models
from db.base_model import BaseModel
from sp_user.models import Users

# Create your models here.
class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="sp_user.Users", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话", max_length=11)
    hcity = models.CharField(verbose_name="省", max_length=100)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, default='')
    harea = models.CharField(verbose_name="区", max_length=100, blank=True, default='')
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False, blank=True)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username