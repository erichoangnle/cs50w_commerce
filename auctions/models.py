from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(null=True)
    image = models.CharField(max_length=200)
    status = models.CharField(max_length=6)
    time = models.DateTimeField(null=True)
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"({self.status}) {self.title} by {self.creator.username} on {self.time}"

class Won(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="winner")
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.user} won {self.item.title} on {self.time}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_log", null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)
    bid = models.IntegerField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.item.title}: ${self.bid} by {self.bidder.username} on {self.time}"

class Comment(models.Model):
    op = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comments", null=True)
    comment = models.CharField(max_length=500, null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.op.username} - {self.time}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="which_user_watchlist")

    def __str__(self):
        return f"{self.user}: {self.item.title} -- ${self.item.starting_bid}"
