# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-10 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0009_auto_20170310_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='weight',
            field=models.IntegerField(null=True, verbose_name='Peso'),
        ),
    ]