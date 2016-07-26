# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0010_auto_20160725_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='last_access_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6700\u8fd1\u4e00\u6b21\u8bbf\u95ee\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
