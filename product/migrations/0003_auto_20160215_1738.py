# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from autoslug.utils import slugify

from django.db import migrations, models
import autoslug.fields
from product.models import Product


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    def gen_slug(apps, schema_editor):
        max_length = Product._meta.get_field('slug').max_length
        for row in Product.objects.all():
            row.slug = slugify(row.name)[:max_length]
            row.save()

    operations = [

        migrations.RunPython(gen_slug),

        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True, max_length=250),
        ),
    ]
