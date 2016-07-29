# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0013_emoji'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_type', models.CharField(default=b'', max_length=255, verbose_name='\u5ba2\u6237\u7aef\u7c7b\u578b')),
                ('version', models.CharField(default=b'', max_length=255, verbose_name='\u5ba2\u6237\u7aef\u7248\u672c')),
                ('os_version', models.CharField(default=b'', max_length=255, verbose_name='\u5ba2\u6237\u7aef\u7cfb\u7edf\u7248\u672c')),
                ('platform', models.CharField(default=b'', max_length=255, verbose_name='\u5e94\u7528\u7684\u53d1\u5e03\u5e73\u53f0')),
                ('device_identifier', models.CharField(default=b'', max_length=255, verbose_name='\u8bbe\u5907\u53f7')),
                ('machine_type', models.CharField(default=b'', max_length=255, verbose_name='\u8bbe\u5907\u578b\u53f7')),
                ('idfa', models.CharField(max_length=255, null=True, verbose_name='iOS idfa', blank=True)),
                ('device_token', models.CharField(max_length=255, null=True, verbose_name='iOS\u63a8\u9001\u8bbe\u5907\u53f7', blank=True)),
                ('push_type', models.IntegerField(null=True, verbose_name='iOS\u63a8\u9001\u8bc1\u4e66\u7c7b\u578b', blank=True)),
                ('xiaomi_push', models.CharField(max_length=255, null=True, verbose_name='\u5c0f\u7c73\u63a8\u9001\u8bbe\u5907\u53f7', blank=True)),
                ('huawei_push', models.CharField(max_length=255, null=True, verbose_name='\u534e\u4e3a\u63a8\u9001\u8bbe\u5907\u53f7', blank=True)),
                ('user', models.ForeignKey(verbose_name='\u5bf9\u5e94host\u7528\u6237', blank=True, to='broadcast.User', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='emoji',
        ),
    ]
