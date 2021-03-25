from django.contrib import admin
from .models import Listing, watchlist, biding, comment, User, replie

class UserAdmin(admin.ModelAdmin):
    fields=["id", "username", "email", "last_login", "date_joined", "alert", "won_auctions", "active_auctions", "money"]
    readonly_fields=["id", "last_login", "date_joined", "won_auctions", "money"]

class ListingAdmin(admin.ModelAdmin):
    fields=["title", "description", "image_url", "id", "author", 
    "created_at", "last_edited", "status", "starting_bid", "current_bid", "current_bider", "winner_bid", "winner", "TotalBiders",  "alert"]
    readonly_fields=["id", "author", "created_at", "last_edited", "starting_bid", "current_bid", "current_bider", "winner_bid", "winner", "TotalBiders", ]
    
class watchlistAdmin(admin.ModelAdmin):
    readonly_fields=["id", "article", "user"]

class bidingAdmin(admin.ModelAdmin):
    readonly_fields=["id", "amount", "bider", "article", "when_bid"]

class commentAdmin(admin.ModelAdmin):
    fields = ["id", "commentary", "author", "article", "article_id", "created_at"]
    readonly_fields = ["id", "author", "article", "article_id", "created_at"]

class replieAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "author", "reply", "article", "comment_replied", "created_at"]


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(watchlist, watchlistAdmin)
admin.site.register(biding, bidingAdmin)
admin.site.register(comment, commentAdmin)
admin.site.register(replie, replieAdmin)




