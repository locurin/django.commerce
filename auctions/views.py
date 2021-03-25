from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import models
from django.forms import ModelForm
from .models import Listing, User, watchlist, biding, comment, replie
from django.contrib.auth.decorators import login_required
from . import util

"""
renders e-commerce's index including every active auction
"""
def index(request):
    # clear user alerts
    user = util.get_user(request)
    User.objects.filter(pk=user.id).update(alert="")
    # get list of listings from database and render it
    listings = util.All_Listings()
    context = {"listings": listings, "user":user}
    return render(request, "auctions/index.html", context)

"""
login user account
"""
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

"""
logout user account
"""
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

"""
register a new user
"""
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

"""
creates a new auction's article and render its page if success
"""
@login_required
def new(request):
    if request.method == "GET":
        return render(request, "auctions/new.html")
    else:
        # add stock description if non is submited
        if not request.POST["description"]:
            description = "Seller didn't add a description to this article."
        else:
            description = util.markdown_translate(request.POST["description"]) 
        # create variables for every other field
        title = request.POST["title"]
        image_url = request.POST["url_image"]
        starting_bid = request.POST["new_listing_starting_bid"]
        category = request.POST["category"]
        user = util.get_user(request)
        alert = "new_article"
        # submit new article
        new_article = Listing(author=user, title=title, description=description, image_url=image_url, 
        starting_bid=starting_bid, category=category, alert=alert) 
        new_article.current_bid = new_article.starting_bid
        new_article.save()
        # update author's active auctions counter
        User.objects.filter(pk=user.id).update(active_auctions=int(user.active_auctions)+1)
        return redirect("listing", title)


"""
redirects to categories
"""
def auctions(request):
    return index(request)

"""
if existing, render a listing page and its information  
"""
def listing(request, title):
    try:
        article = Listing.objects.get(title=title)
        # clear article's alert
        Listing.objects.filter(pk=article.id).update(alert="")
        # check if listing is in user's watchlist or not
        In_watchlist = util.CheckIfInWatchlist(request, article)
        if In_watchlist:
            watchlisted = util.GetWatchlistID(request, article)
        else:
            watchlisted = None
        # check if user created the listing
        is_author = util.CheckIfAuthor(request, article)
        # get article's comments and replies
        comments = util.get_comments(article)
        replies = util.get_replies(article)
        # render result
        context = {"article":article, "WatchlistOrNot":In_watchlist, "watchlist":watchlisted,
         "is_author":is_author, "comments":comments, "replies":replies}
        return render(request, "auctions/article.html", context)
    except Listing.MultipleObjectsReturned:
        # if multiple results matchs the title, render all possible listings
        results = Listing.objects.filter(title=title)
        listings = []
        for result in results:
            listings.append(result)
        context = {"listings":listings, "query":title}
        return render(request, "auctions/results.html", context)
        # renders 404 page if no listing is found
    except Listing.DoesNotExist:
        return render(request, "auctions/not_found.html")

"""
if POST requested, adds/removes a listing from the watchlist page. If GET requestes, renders watchlist
"""
@login_required       
def watchlist_control(request):
    if request.method == "POST":
        # adds listing to watchlist
        if "add_to_watchlist" in request.POST:
            article_id = request.POST["add_to_watchlist"]
            article = Listing.objects.get(pk=article_id)
            user = util.get_user(request)
            new_watch = watchlist(article=article, user=user)
            new_watch.save()
            return redirect("listing", article.title)
        # removes listing from watchlist
        else:
            watchlist_id = request.POST["remove_from_watchlist"]
            WatchlistToBeRemoved = watchlist.objects.get(id=watchlist_id)
            article = WatchlistToBeRemoved.article
            WatchlistToBeRemoved.delete()
            return redirect("listing", article)
    else:
        # render watchlist
        user = util.get_user(request)
        watched_articles = watchlist.objects.filter(user_id=user.id)
        listings = []
        for article in watched_articles:
            listings.append(Listing.objects.get(pk=article.article_id))
        context = {"watched_articles":listings}
        return render(request, "auctions/watchlist.html", context)

"""
render a list of all available categories with links to redirect to them  
"""
def categories_list(request):
    categories = Listing.ListOf_Categories
    context = {"categories":categories}
    return render(request, "auctions/categories.html", context)

"""
display all listings regarding the requested category 
"""
def category_display(request, category):
    articles = Listing.objects.filter(category=category.capitalize())
    listings = []
    Empty = False
    for article in articles:
        listings.append(article)
    # if no articles in the category, instead renders a warning message
    if not listings:
        Empty = True
    context = {"listings":listings, "category":category, "Empty":Empty}
    return render(request, "auctions/category.html", context)

"""
Closes auction if requested by listing's author
"""
@login_required 
def close(request):
    if request.method == "POST":
        # close auction and set winner
        article_id = request.POST["close_auction"]
        article = Listing.objects.get(pk=article_id)
        # if no bids were placed, erase the auction from database and update user alert and active auctions counter
        if article.TotalBiders == 0:
            article.delete()
            user = article.author
            alert = "listing_deleted"
            User.objects.filter(pk=user.id).update(alert=alert, active_auctions=int(user.active_auctions)-1)
            return redirect("index")
        Listing.objects.filter(pk=article_id).update(status="Closed", winner=article.current_bider, 
        winner_bid=article.current_bid, current_bid=None, current_bider=None)
        # updates "last updated" field on more time to display on closed auction 
        close_update = Listing.objects.get(pk=article_id)
        close_update.save()
        # updates seller active auctions and money amount
        seller = article.author
        User.objects.filter(pk=seller.id).update(active_auctions=int(seller.active_auctions)-1,
        money=seller.money + int(article.current_bid))
        # update buyer's won auctions counter and money amount
        buyer = article.current_bider
        User.objects.filter(pk=buyer.id).update(won_auctions=int(buyer.won_auctions)+1, 
        money=buyer.money - int(article.current_bid))
        # eliminates watchlists regarding closed listing
        watchlist.objects.filter(article=article).delete()
        return redirect("listing", article.title)
    else:
        return render(request, "auctions/not_found.html")

"""
Deletes auction if requested by listing's author
"""
@login_required 
def delete(request):
    if request.method == "POST":
        # deletes listing
        article_id = request.POST["delete_auction"]
        article = Listing.objects.get(pk=article_id)
        article.delete()
        # updates user's alert and active auctions counter
        user = util.get_user(request)
        alert = "listing_deleted"
        User.objects.filter(pk=user.id).update(alert=alert, active_auctions=int(user.active_auctions)-1)
        # redirect to index
        return redirect("index")


"""
Updates bidings and biders data 
"""
@login_required
def bids(request):
    if request.method == "POST":
        bider = util.get_user(request)
        amount = int(request.POST["amount"])
        article_id = request.POST["article"]
        article = Listing.objects.get(pk=article_id)
        TotalBiders = int(article.TotalBiders)
        # prevent seller tu bid on its own auctions
        if bider == article.author:
            alert = "own_auction"
            Listing.objects.filter(pk=article.id).update(alert=alert)
            return redirect("listing", article.title)
        #check if user has enough money to pay his bid
        if bider.money < amount:
            alert = "not_enough_money"
            Listing.objects.filter(pk=article.id).update(alert=alert)
            return redirect("listing", article.title)
        # if first bid, accept equal value of starting bid as a valid bid
        if TotalBiders == 0 and amount >= article.current_bid:
            util.upload_biding(article, amount, TotalBiders, bider)
            alert = "bid_success"
            Listing.objects.filter(pk=article.id).update(alert=alert)
            return redirect("listing", article.title)
        # if not first bid, only accept bids higher than current
        elif amount > article.current_bid: 
            util.upload_biding(article, amount, TotalBiders, bider)
            alert = "bid_success"
            Listing.objects.filter(pk=article.id).update(alert=alert)
            return redirect("listing", article.title)
    else:
        return render(request, "auctions/not_found.html")

"""
adds comments made on listings to database
"""
@login_required
def comment_handler(request):
    if request.method == "POST":
        commenter = util.get_user(request)
        article_id = request.POST["article"]
        article = Listing.objects.get(pk=article_id)
        print(request.POST["comment_textarea"])
        if request.POST["comment_textarea"].isspace():
            alert = "empty_comment"
            Listing.objects.filter(pk=article_id).update(alert=alert)
            return redirect("listing", article.title)
        else:
            commentary = str(request.POST["comment_textarea"])
        comment.objects.create(commentary=commentary, author = commenter, article = article)
        alert = "comment_submited"
        Listing.objects.filter(pk=article.id).update(alert=alert)
        return redirect("listing", article.title)
    else:
        return render(request, "auctions/not_found.html")

"""
adds replies made on listing's comments to database
"""
@login_required
def replies_handler(request):
    if request.method == "POST":
        comment_id = request.POST["comment_id_to_reply"]
        commentary = comment.objects.get(pk=comment_id)
        article = commentary.article
        if request.POST["reply_comment"].isspace():
            alert = "empty_reply"
            Listing.objects.filter(pk=article.id).update(alert=alert)
            return redirect("listing", article.title)
        else:
            reply = str(request.POST["reply_comment"])
        author = util.get_user(request)
        replie.objects.create(reply=reply, author=author, article=article, comment_replied=commentary)
        alert = "reply_submited"
        Listing.objects.filter(pk=article.id).update(alert=alert)
        return redirect("listing", article.title)
    else:
        return render(request, "auctions/not_found.html")

"""
displays a requested user's profile page and data
"""
@login_required
def profile_all(request, username):
    user = User.objects.get(username=username)
    User.objects.filter(pk=user.id).update(alert="")
    active_listings = Listing.objects.filter(author=user, status="Active")
    context = {"profile":user, "active_listings":active_listings}
    return render(request, "auctions/profile.html", context)

"""
displays active user profile 
"""
@login_required
def profile(request):
    user = util.get_user(request)
    return profile_all(request, user.username)
    
"""
handles user's password and username update
"""
@login_required
def profile_update(request):
    if request.method == "POST":
        user = util.get_user(request)
        if "new_username" in request.POST:
            new_username = request.POST["new_username"]
            repeat_new_username = request.POST["repeat_new_username"]
            return util.change_username(user, new_username, repeat_new_username)
        else: 
            new_pass = request.POST["new_password"]
            repeat_new_pass = request.POST["repeat_new_password"]
            return util.change_password(user, new_pass, repeat_new_past)





        


        
    
    