# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0005_auto_20160723_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(null=True, verbose_name='\u6027\u522b', blank=True),
            preserve_default=True,
        ),
    ]
