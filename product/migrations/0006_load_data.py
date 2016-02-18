# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.core.management import call_command


class Migration(migrations.Migration):

    def load_data(apps, schema_editor):
        call_command("loaddata", "initial_data.json")

    dependencies = [
        ('product', '0005_product_likes'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
