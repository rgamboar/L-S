# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20170106_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='repAddress',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='repEmail',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='repPhone',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
