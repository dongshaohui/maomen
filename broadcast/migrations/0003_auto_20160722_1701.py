# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0002_userchannelrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='TencentCloudUsreInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_tencent_id', models.CharField(default=b'', max_length=255, verbose_name='\u7528\u6237\u817e\u8baf\u4e91ID')),
                ('user_sig', models.CharField(default=b'', max_length=255, verbose_name='\u817e\u8baf\u4e91\u7528\u6237\u7b7e\u540d')),
                ('tim_id', models.CharField(default=b'', max_length=255, verbose_name='\u817e\u8baf\u4e91\u7528\u6237\u6807\u8bc6')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
                ('user', models.ForeignKey(verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_id',
            field=models.IntegerField(default=0, verbose_name='\u9891\u9053ID'),
            preserve_default=True,
        ),
    ]
