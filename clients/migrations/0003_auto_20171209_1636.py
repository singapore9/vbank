# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20171209_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(),
        ),
    ]
