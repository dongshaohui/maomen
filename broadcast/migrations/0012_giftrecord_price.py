# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0011_channel_last_access_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftrecord',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='\u9001\u793c\u94b1\u6570'),
            preserve_default=True,
        ),
    ]
