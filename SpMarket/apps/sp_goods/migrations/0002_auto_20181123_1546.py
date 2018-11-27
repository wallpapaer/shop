# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 07:46
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sp_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('img_url', models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='相册图片地址')),
            ],
            options={
                'verbose_name': '商品相册管理',
                'verbose_name_plural': '商品相册管理',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('sku_name', models.CharField(max_length=100, verbose_name='商品SKU名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='商品的简介')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='价格')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sale_num', models.IntegerField(default=0, verbose_name='销量')),
                ('logo', models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='封面图片')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.Category', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品SKU管理',
                'verbose_name_plural': '商品SKU管理',
            },
        ),
        migrations.CreateModel(
            name='GoodsSPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('spu_name', models.CharField(max_length=20, verbose_name='商品SPU名称')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods_spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSPU', verbose_name='商品SPU'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSKU', verbose_name='SKU商品'),
        ),
    ]