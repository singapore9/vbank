# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20171106_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.PositiveIntegerField(choices=[(8, 'Manager'), (1, 'Client'), (0, 'OUT_OF_ROLE')], default=0),
        ),
    ]
