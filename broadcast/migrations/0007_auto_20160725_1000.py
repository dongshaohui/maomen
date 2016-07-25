# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0006_auto_20160724_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='audience_num',
            field=models.IntegerField(default=0, verbose_name='\u5f53\u524d\u9891\u9053\u89c2\u770b\u4eba\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_status',
            field=models.IntegerField(default=0, verbose_name='\u9891\u9053\u72b6\u6001'),
            preserve_default=True,
        ),
    ]
