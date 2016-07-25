# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0004_channel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftrecord',
            name='user',
        ),
        migrations.AddField(
            model_name='giftrecord',
            name='from_user',
            field=models.ForeignKey(related_name='from_user', verbose_name='\u9001\u793c\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftrecord',
            name='to_user',
            field=models.ForeignKey(related_name='to_user', verbose_name='\u6536\u793c\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_type',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u7b2c\u4e09\u65b9\u8d26\u53f7\u7c7b\u578b'),
            preserve_default=True,
        ),
    ]
