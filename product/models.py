from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, max_length=250)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=11)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes')
    like_amount = models.PositiveIntegerField(default=0)

    @property
    def total_likes(self):
        return self.likes.count()

    def set_like_amount(self):
        self.like_amount = self.total_likes

    def __unicode__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.like_amount = self.total_likes
        super(Product, self).save(*args, **kwargs)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=150)
    email = models.EmailField()
    comment = models.CharField(max_length=500, null=False)
    product = models.ForeignKey(Product, related_name='comments')


