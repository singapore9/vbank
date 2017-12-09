# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 09:46
from __future__ import unicode_literals

import custom_auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now, validators=[custom_auth.validators.not_future_validator, custom_auth.validators.age_validator]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='first_name',
            field=models.CharField(max_length=30, validators=[custom_auth.validators.NameValidator('First name')], verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='last_name',
            field=models.CharField(max_length=30, validators=[custom_auth.validators.NameValidator('Last name')], verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='middle_name',
            field=models.CharField(max_length=30, validators=[custom_auth.validators.NameValidator('Middle name')], verbose_name='middle name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='residence_address',
            field=models.CharField(max_length=255, verbose_name='residence address'),
        ),
    ]
