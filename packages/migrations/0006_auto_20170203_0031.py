# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-03 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0005_pickup'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickup',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pickUpPackage', to='packages.Package', verbose_name='Guia de flete'),
        ),
        migrations.AlterField(
            model_name='pickup',
            name='quantity',
            field=models.IntegerField(verbose_name='Cantidad'),
        ),
    ]
