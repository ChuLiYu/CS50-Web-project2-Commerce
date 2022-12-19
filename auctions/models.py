from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_user"


# category

# Title, strart_bid, pic, description, bid_history, category,  creator_id, is_active
class Listing(models.Model):
    CATEGORY_CHOICES = (
        ("1", "Apparel and accessories"),
        ("2", "Auto and parts"),
        ("3", "Book, music and video"),
        ("4", "Computer, technology and eletronics"),
        ("5", "Furniture"),
        ("6", "Health, personal care and beauty"),
        ("7", "Office"),
        ("8", "Toys and hobby"),
        ("9", "Other"),
    )
    title = models.TextField(max_length=64)
    description = models.TextField(max_length=200)
    start_bid = models.FloatField()
    img = models.ImageField(blank=True, null=True, upload_to="image")
    img_link = models.URLField(blank=True, null=True)
    category = models.TextField(max_length=64, choices=CATEGORY_CHOICES)
    creator_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_user_id"
    )
    bidding_id = models.ManyToManyField(
        User, through="Bidding", related_name="listing_bidding_id", blank=True
    )
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    watchlist_id = models.ManyToManyField(
        User, through="Watchlist", related_name="listing_watchlist_id", blank=True
    )

    class Meta:
        db_table = "listing"

    def __str__(self):
        return f"{self.title} - {self.description} -{self.start_bid}"


# creator_id, listening_id, bidding_price, created_time
class Bidding(models.Model):
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bidding_listing_id"
    )
    bidding_price = models.FloatField()
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table = "bidding"


# listing_id, comment_str, created_time, creator_id
class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_str = models.TextField()
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "comment"


# creator_id, listing_id,
class Watchlist(models.Model):
    creator_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist_creator_id"
    )
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watchlist_listing_id"
    )

    class Meta:
        db_table = "watchlist"
        unique_together = ("creator_id", "listing_id")

    def __str__(self):
        return f"{self.creator_id} - {self.listing_id}"
