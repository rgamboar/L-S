# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-22 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0014_auto_20170322_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='boleta',
            field=models.PositiveIntegerField(null=True, verbose_name='Boleta'),
        ),
        migrations.AlterField(
            model_name='package',
            name='old_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Guia anterior'),
        ),
        migrations.AlterField(
            model_name='package',
            name='quantity',
            field=models.PositiveIntegerField(null=True, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='package',
            name='rate',
            field=models.PositiveIntegerField(verbose_name='Tarifado'),
        ),
        migrations.AlterField(
            model_name='package',
            name='weight',
            field=models.PositiveIntegerField(null=True, verbose_name='Peso'),
        ),
    ]
