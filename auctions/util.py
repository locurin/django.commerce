#complementary functions for views.py

from .models import Listing, watchlist, biding, comment, replie, User
from markdown2 import Markdown
from django.shortcuts import render, redirect
from django.db import IntegrityError


"""
returns current user as an queryable object
"""
def get_user(request):
    current_user = request.user
    return current_user

"""
returns a list with every listing article object
"""
def All_Listings():
    listings = Listing.objects.all()
    return listings

"""
checks if requested article its on user's watchlist
"""
def CheckIfInWatchlist(request, article):
    user = get_user(request)
    try:
        watchlist.objects.get(article=article, user=user)
        In_watchlist = True
        return In_watchlist 
    except watchlist.DoesNotExist:
        In_watchlist = False
        return In_watchlist


"""
gets watchlisted database's ID for requested query
"""
def GetWatchlistID(request, article):
    user = get_user(request)
    return watchlist.objects.get(article=article, user=user)
    

"""
checks if user is author of the article
"""
def CheckIfAuthor(request, article):
    user = get_user(request)
    if f"{article.author}" == f"{user.username}":
        return True
    else:
        return False

"""
updates listing's bidding data to databases
"""
def upload_biding(article, amount, TotalBiders, bider):
    Listing.objects.filter(pk=article.id).update(current_bid=amount, current_bider=bider, 
    TotalBiders=TotalBiders+1)
    NewBid = biding.objects.create(amount=amount, bider=bider, article=article)

"""
gets comments regarding requested article
"""
def get_comments(article):
    return comment.objects.filter(article=article)

"""
gets comment replies regarding requested article
"""
def get_replies(article):
    return replie.objects.filter(article=article)
    
"""
translate from markdown to html syntax
"""
def markdown_translate(description):
    translator = Markdown()
    return translator.convert(description)

"""
change user's username
"""
def change_username(user, username, repeat_username):
    taken_username_list = User.objects.all().values("username")
    try:
        if username != user.username:
            allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@.+-_"))
            validation = set((username))
            if validation.issubset(allowed_chars):
                if len(username) >= 4: 
                    if username == repeat_username:
                        alert = "username_changed"
                        User.objects.filter(pk=user.id).update(username=username, alert=alert)
                        return redirect(f"../../profile/{username}")
                    else:
                        alert = "username_dont_match"
                        User.objects.filter(pk=user.id).update(alert=alert)
                        return redirect(f"../../profile/{user.username}")
                else:
                    alert = "username_too_short"
                    User.objects.filter(pk=user.id).update(alert=alert)
                    return redirect(f"../../profile/{user.username}")
            else:
                alert = "characters_not_allowed"
                User.objects.filter(pk=user.id).update(alert=alert)
                return redirect(f"../../profile/{user.username}")
        else:
            alert = "current_username"
            User.objects.filter(pk=user.id).update(alert=alert)
            return redirect(f"../../profile/{user.username}")
    except IntegrityError:
            alert = "username_taken"
            User.objects.filter(pk=user.id).update(alert=alert)
            return redirect(f"../../profile/{user.username}")