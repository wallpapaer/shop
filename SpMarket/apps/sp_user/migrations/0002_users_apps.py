# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sp_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='apps',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]