# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0009_auto_20160725_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tencentcloudusreinfo',
            name='user_sig',
            field=models.CharField(default=b'', max_length=5000, verbose_name='\u817e\u8baf\u4e91\u7528\u6237\u7b7e\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userchannelrecord',
            name='status',
            field=models.IntegerField(default=1, verbose_name='\u6536\u770b\u9891\u9053\u72b6\u6001'),
            preserve_default=True,
        ),
    ]
