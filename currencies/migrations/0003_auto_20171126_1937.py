# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-26 19:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_auto_20171126_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sale', models.FloatField(help_text='against the BYN')),
                ('purchase', models.FloatField(help_text='against the BYN')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.RemoveField(
            model_name='currency',
            name='purchase_rate',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='sale_rate',
        ),
        migrations.AddField(
            model_name='currencyrate',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='currencies.Currency'),
        ),
    ]
