# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-11-16 06:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0097_auto_20201109_1237'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='proposalfilmingparks',
            unique_together=set([('proposal', 'park')]),
        ),
    ]
