# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0008_auto_20160725_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interactchannelrecord',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='interactchannelrecord',
            name='user',
        ),
        migrations.DeleteModel(
            name='InteractChannelRecord',
        ),
    ]
