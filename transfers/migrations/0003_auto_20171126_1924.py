# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-26 19:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0002_externaltransfer_is_favourite'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CardTransfer',
            new_name='InternalTransfer',
        ),
    ]
