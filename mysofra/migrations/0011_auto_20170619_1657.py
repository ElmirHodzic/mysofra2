# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-19 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysofra', '0010_auto_20170619_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(default=b'passwd', max_length=200),
        ),
    ]
