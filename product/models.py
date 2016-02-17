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

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.modified_at = timezone.now()
        super(Product, self).save(*args, **kwargs)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=150)
    email = models.EmailField()
    comment = models.CharField(max_length=500, null=False)
    product = models.ForeignKey(Product, related_name='comments')


