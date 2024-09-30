from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    imageUrl = models.CharField(max_length=1024)
    start_price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

