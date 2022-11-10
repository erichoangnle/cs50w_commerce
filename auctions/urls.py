from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing_page/<str:id>", views.listing_page, name="listing_page"),
    path("add_to_watchlist/<str:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("delete_watchlist/<str:item_id>", views.delete_watchlist, name="delete_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listings/<str:name>", views.category_listings, name="category_listings"),
    path("bid/<str:item_id>", views.bid, name="bid"),
    path("close_listing/<str:id>", views.close_listing, name="close_listing"),
    path("won/<str:id>", views.won, name="won")
]
