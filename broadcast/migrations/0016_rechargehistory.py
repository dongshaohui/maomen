# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('broadcast', '0015_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='RechargeHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(verbose_name='\u5bf9\u5e94\u9879\u76ee', blank=True, to='broadcast.Item', null=True)),
                ('user', models.ForeignKey(verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
