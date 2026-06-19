# -*- coding: utf-8 -*-
# Generated manually
from __future__ import unicode_literals

from django.db import migrations


def add_privacy_policy_url(apps, schema_editor):
    GlobalSettings = apps.get_model('commercialoperator', 'GlobalSettings')
    
    # Create the GlobalSettings entry with default value if it doesn't exist
    if not GlobalSettings.objects.filter(key='privacy_policy_url').exists():
        GlobalSettings.objects.create(
            key='privacy_policy_url',
            value='https://www.dbca.wa.gov.au/privacy'
        )


def remove_privacy_policy_url(apps, schema_editor):
    GlobalSettings = apps.get_model('commercialoperator', 'GlobalSettings')
    GlobalSettings.objects.filter(key='privacy_policy_url').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0131_auto_20260318_1153'),
    ]

    operations = [
        migrations.RunPython(add_privacy_policy_url, remove_privacy_policy_url),
    ]
