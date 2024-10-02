from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlisted_by")


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    imageUrl = models.CharField(max_length=1024)
    start_price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="listings_owned")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="listings_in_category")
    last_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name="last_bid_listing")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name="won_listings")


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    time_of_posting = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    time_of_posting = models.DateTimeField(auto_now_add=True)

