# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0014_auto_20160729_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.FloatField(default=0.0, verbose_name='\u91d1\u989d')),
                ('momentMoney', models.FloatField(default=0.0, verbose_name='\u865a\u62df\u91d1\u989d')),
                ('note', models.CharField(default=b'', max_length=255, verbose_name='\u540d\u79f0')),
                ('IAPId', models.CharField(max_length=255, null=True, verbose_name='IAPId', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
