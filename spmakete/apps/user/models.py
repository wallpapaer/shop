from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=100,verbose_name='用户名')
    password = models.DateField(verbose_name='密码')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username