# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-26 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='externaltransfer',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]