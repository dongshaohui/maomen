# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0016_rechargehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppleReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receipt_md5', models.CharField(default=b'', max_length=255, verbose_name='\u51ed\u8bc1\u7684md5')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
