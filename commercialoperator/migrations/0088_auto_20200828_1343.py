# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-28 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0087_auto_20200818_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposaltype',
            name='name',
            field=models.CharField(choices=[('Commercial operations', 'Commercial operations'), ('Event', 'Event'), ('Filming', 'Filming')], default='T Class', max_length=64, verbose_name='Application name (eg. T Class, Filming, Event, E Class)'),
        ),
    ]
