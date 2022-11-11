from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import *

from .models import User


def index(request):
    """
    Render all active listings in database and sort by time created.
    """
    listings = Listing.objects.filter(status="active").order_by("-time")
    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    """
    User log in.
    """
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


def logout_view(request):
    """
    User log out.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Register new user.
    """
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


@login_required
def add_listing(request):
    """
    If request method is POST, create a new listing according to user's
    inputs, save new listing to database, and redirect user to newly
    created listing page. If request method is GET, render add listing
    form.
    """
    if request.method == "POST":
        if request.POST["title"] and request.POST["starting_bid"] and request.POST["category"]:
            listing = Listing(
                creator = request.user,
                title = request.POST["title"],
                starting_bid = request.POST["starting_bid"],
                current_price = request.POST["starting_bid"],
                description = request.POST["description"],
                image = request.POST["image"],
                status = 'active',
                time = datetime.now().replace(microsecond=0),
                category = request.POST["category"].capitalize()
            )
            listing.save()
            return HttpResponseRedirect(f"/listing_page/{listing.id}")
    else:
        return render(request, "auctions/add_listing.html")


def listing_page(request, id):
    """
    Page template for individual listing. If request method is GET,
    render lsting informations, listing image, and listing comments
    if any. If request method is POST, user has entered a comment
    on this listing. Save comment to database and redirect user to
    the same listing page with new comment added.
    """
    if request.method == "POST":
        comment = Comment(
            op = request.user,
            item = Listing.objects.get(pk=id),
            comment = request.POST["comment"],
            time = datetime.now().replace(microsecond=0)
        )
        comment.save()
        return HttpResponseRedirect(f"/listing_page/{id}")
    else:
        item = Listing.objects.get(pk=id)
        comments = Comment.objects.filter(item=item).order_by('-time')

        return render(request, "auctions/listing_page.html", {
            'listing': Listing.objects.get(pk=id),
            'comments': comments
        })


@login_required
def bid(request, item_id):
    """
    Process user's bid on listing. There is no HTML template for this function.
    If bid is valid, save bid to database and redirect user to the same listing
    page. If bid is not valid, render the same listing page with an error message.
    """
    if request.method == 'POST':
        item = Listing.objects.get(pk=item_id)
        bids = Bid.objects.filter(item=item).order_by('-bid')
        new_bid = int(request.POST["bid"])

        if bids: current_price = int(bids[0].bid)
        else: current_price = int(item.starting_bid)

        if new_bid > current_price:
            bid = Bid(
                item = item,
                bidder = request.user,
                bid = request.POST["bid"],
                time = datetime.now().replace(microsecond=0)
            )
            bid.save()
            item.current_price = new_bid
            item.save()           
            return HttpResponseRedirect(f"/listing_page/{item_id}")
        else:
            return render(request, "auctions/listing_page.html", {
                'listing': Listing.objects.get(pk=item_id),
                'comments': Comment.objects.filter(item=item),
                'error_message': 'Invalid bid!'
            })


@login_required
def close_listing(request, id):
    """
    User can onlye access this function if he/she is the creator of a listing.
    Change the listing status from active to closed. Whoever has the highest
    bid on said listing will be the winner.
    """
    item = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(item=item).order_by('-bid')
    item.status = 'closed'
    item.save()
    if bids:
        won = Won(
            user = bids[0].bidder,
            item = item,
            time = datetime.now().replace(microsecond=0)
        )
        won.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def won(request, id):
    """
    Render a template with all items won by user.
    """
    user = User.objects.get(pk=id)
    listings = user.won.all()
    return render(request, "auctions/won.html", {
        'listings': listings
    })


@login_required
def add_to_watchlist(request, listing_id):
    """
    This function is only accessible to user who is not the creator of a
    listing. It will add current listing to user's watchlist and redirect
    user to Watchlist page.
    """
    user = User.objects.get(pk=request.user.id)
    item = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist(user = user, item = item)
    watchlist.save()
    return HttpResponseRedirect(f"/watchlist/{user.id}")


@login_required
def watchlist(request, user_id):
    """
    Render a watchlist page with all listing user currently have in watchlist.
    """
    user = User.objects.get(pk=user_id)
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })


@login_required
def delete_watchlist(request, item_id):
    """
    Delete an item from user's watchlist.
    """
    item = Watchlist.objects.get(item=item_id)
    item.delete()
    return HttpResponseRedirect(f"/watchlist/{request.user.id}")


def categories(request):
    """
    Render a page that list all categories with active listings.
    """
    categories = Listing.objects.filter(status='active').values_list("category", flat=True).distinct()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


def category_listings(request, name):
    """
    Render a page that display only listings in a certain category.
    """
    listings = Listing.objects.filter(status='active', category=name)
    return render(request, "auctions/category_listings.html", {
        'listings': listings,
        'name': name
    })
