from autoslug.utils import slugify
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, max_length=250)
    description = models.TextField(blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.modified_at = timezone.now()
        super(Product, self).save(*args, **kwargs)




