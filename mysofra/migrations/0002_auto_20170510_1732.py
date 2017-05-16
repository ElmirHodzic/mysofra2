# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-10 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysofra', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mysofraMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(blank=True, default=b'', max_length=100)),
                ('message', models.TextField()),
                ('mail_from', models.CharField(default=b'checkouts@mysofra.at', max_length=100)),
                ('mail_to', models.CharField(default=b'orders@mysofra.at', max_length=100)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[(b'1', b'Huhnerfleisch'), (b'2', b'Rindfleisch')], default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]