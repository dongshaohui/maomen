# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0003_auto_20160722_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
    ]
