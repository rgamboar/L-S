# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-12 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0016_auto_20170112_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='deliverDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='deliverer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packageDeliverer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='transmitDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='transmitter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packageTransmitter', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]