# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-11-06 05:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0097_auto_20201106_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oraclecode',
            name='park',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='oracle_code_obj', to='commercialoperator.Park'),
        ),
    ]
