# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 22:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20170106_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='truck',
            old_name='is_own',
            new_name='is_rent',
        ),
    ]
