# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-02 22:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_remove_package_transmitdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='startAddress',
        ),
    ]
