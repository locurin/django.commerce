from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("auctions/", views.auctions, name="auctions"),
    path("auctions/<str:title>/", views.listing, name="listing"),
    path("watchlist", views.watchlist_control, name="watchlist"),
    path("categories", views.categories_list, name="categories"),
    path("categories/<str:category>/", views.category_display, name="categories/category"),
    path("close", views.close, name="close"),
    path("delete", views.delete, name="delete"),
    path("bids", views.bids, name="bids"),
    path("comment", views.comment_handler, name="comment"),
    path("replies", views.replies_handler, name="replies"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.profile_all, name="profile_all"),
    path("profile_update", views.profile_update, name="profile_update")
]
