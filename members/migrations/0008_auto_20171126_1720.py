# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-26 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20171126_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardtransfer',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='cardtransfer',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='externaltransfer',
            name='sender',
        ),
        migrations.DeleteModel(
            name='CardTransfer',
        ),
        migrations.DeleteModel(
            name='ExternalTransfer',
        ),
    ]
