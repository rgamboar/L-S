# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-03 00:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_remove_package_startaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='is_transmitter',
        ),
        migrations.RemoveField(
            model_name='package',
            name='transmitter',
        ),
    ]
