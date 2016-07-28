# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0012_giftrecord_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='emoji',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u540d\u79f0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
