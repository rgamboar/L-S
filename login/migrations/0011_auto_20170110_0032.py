# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-10 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_package_is_transmitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='finishAddress',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='startAddress',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
