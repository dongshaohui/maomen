# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=0.0, verbose_name='\u8d26\u6237\u4f59\u989d')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='\u9891\u9053\u6807\u9898')),
                ('cover', models.CharField(default=b'', max_length=255, verbose_name='\u9891\u9053\u5c01\u9762')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u540d\u79f0')),
                ('price', models.FloatField(default=0.0, verbose_name='\u793c\u7269\u5355\u4ef7')),
                ('url', models.CharField(default=b'', max_length=255, verbose_name='\u793c\u7269\u94fe\u63a5')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GiftRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=1, verbose_name='\u9001\u793c\u6570\u91cf')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
                ('gift', models.ForeignKey(related_name='gc_gift', verbose_name='\u5bf9\u5e94\u793c\u7269', blank=True, to='broadcast.Gift', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, verbose_name='\u8bdd\u9ea6\u4f4d\u7f6e')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
                ('channel', models.ForeignKey(related_name='interact_channel', verbose_name='\u5bf9\u5e94\u9891\u9053', blank=True, to='broadcast.Channel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.CharField(default=b'', max_length=255, verbose_name='\t\u7b2c\u4e09\u65b9\u8d26\u53f7\u7c7b\u578b')),
                ('third_party_id', models.CharField(default=b'', max_length=255, verbose_name='\u7b2c\u4e09\u65b9\u6807\u8bc6')),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u6635\u79f0')),
                ('sex', models.CharField(default=b'', max_length=255, verbose_name='\u6027\u522b')),
                ('avatar', models.CharField(default=b'', max_length=255, verbose_name='\u5934\u50cf')),
                ('city', models.CharField(default=b'', max_length=255, verbose_name='\u57ce\u5e02')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='interact',
            name='user',
            field=models.ForeignKey(related_name='interact_user', verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftrecord',
            name='user',
            field=models.ForeignKey(related_name='gc_gift', verbose_name='\u5bf9\u5e94\u7528\u6237', blank=True, to='broadcast.User', null=True),
            preserve_default=True,
        ),
    ]
