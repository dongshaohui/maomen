# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0007_auto_20160725_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteractChannelRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, verbose_name='\u558a\u9ea6\u4f4d\u7f6e')),
                ('status', models.IntegerField(default=0, verbose_name='\u558a\u9ea6\u72b6\u6001')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
                ('channel', models.ForeignKey(verbose_name='\u5bf9\u5e94\u9891\u9053', blank=True, to='broadcast.Channel', null=True)),
                ('user', models.ForeignKey(verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userchannelrecord',
            name='position',
        ),
        migrations.AlterField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(verbose_name='\u5bf9\u5e94host\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(default=1, verbose_name='\u6027\u522b'),
            preserve_default=True,
        ),
    ]
