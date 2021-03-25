from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db import models


class User(AbstractUser):
    alert = models.CharField(max_length=64, default="", blank=True)
    won_auctions = models.IntegerField(default=0)
    active_auctions = models.IntegerField(default=0)
    money = models.IntegerField(default=4000)

class Listing(models.Model):
    # general info
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    alert = models.CharField(max_length=64, default="", blank=True)
    # status
    Active = "Active"
    Closed = "Closed"
    STATUS = [(Active, "Active"), (Closed, "Closed")]
    status = models.CharField(choices=STATUS, max_length=20, default="Active")
    # bidings 
    starting_bid = models.IntegerField(default=0)
    current_bid = models.IntegerField(default=0, null=True)
    winner_bid = models.IntegerField(default=0)
    current_bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_bider", default="", null=True)
    TotalBiders = models.IntegerField(default=0)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", default="", null=True)
    # categories
    Fashion = "Fashion"
    Electronics = "Electronics"
    Gaming = "Gaming"
    Toys = "Toys"
    House = "House"
    Garden = "Garden"
    Groceries = "Groceries"
    Vehicles = "Vehicles"
    Music = "Music"
    Pets = "Pets"
    Sports = "Sports"
    CATEGORIES = [
        (Fashion, "Fashion"),
        (Electronics, "Electronics"),
        (Gaming, "Gaming"),
        (Toys, "Toys"),
        (House, "House"),
        (Garden, "Garden"),
        (Groceries, "Groceries"),
        (Vehicles, "Vehicles"),
        (Music, "Music"),
        (Pets, "Pets"),
        (Sports, "sports")
    ]
    # IMPORTANT: Update this list everytime a new category is added above
    ListOf_Categories = [Fashion, Electronics, Gaming, Toys, House, Garden, Groceries, Vehicles, Music, Pets, Sports]
    category = models.CharField(choices=CATEGORIES, max_length=20)

    def __str__(self):
        if self.status == "Active":
            return "{}".format(self.title)
        else:
            return "{} [CLOSED]".format(self.title)

class watchlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    article = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="booked_article", default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_user", default="")
    def __str__(self):
        return "{} watched by {}".format(self.article, self.user)

class biding(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    amount = models.IntegerField()
    bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider", default="")
    article = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="article", default="")
    when_bid =  models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} bid on {} for ${}".format(self.bider, self.article, self.amount)

class comment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    commentary = models.TextField(max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    article = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="messages", default="")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} made a comment on {}".format(self.author, self.article)

class replie(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    reply = models.TextField(max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    article = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="replies_to_comments", default="")
    comment_replied = models.ForeignKey(comment, on_delete=models.CASCADE, related_name="messages", default="")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} replied a comment in {}".format(self.author, self.article)