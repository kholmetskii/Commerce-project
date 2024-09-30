from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Category, Listing

from .models import User


def index(request):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        selected_categories = list(map(int, selected_categories))
        listings = Listing.objects.filter(category__id__in=selected_categories, is_active=True)
    else:
        listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/active_listings.html", {
        "categories": categories,
        "listings": listings,
        "selected_categories": selected_categories
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


def create_listing(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "auctions/create_listing.html", {
                "categories": categories
            })
        else:
            new_listing = Listing(
                title=request.POST['title'],
                description=request.POST['description'],
                imageUrl=request.POST['imageURL'],
                start_price=float(request.POST['price']),
                category=Category.objects.get(name=request.POST['category']),
                owner=request.user
            )
            new_listing.save()
            return redirect('index')
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": categories,
            "error": "You must be sign in."
        })


def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        user = request.user
        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        return redirect('view_listing', listing_id=listing_id)
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "error": "You must be sign in."
        })


def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def make_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        bid_amount = float(request.POST["bid"])
        if bid_amount > (listing.current_bid or listing.price):
            new_bid = Bid.objects.create(
                listing=listing,
                user=request.user,
                bid_amount=bid_amount
            )
            listing.current_bid = bid_amount
            new_bid.save()
            return redirect('view_listing', listing_id=listing.id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "error": "Your bid must be higher than the current bid."
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "error": "You must be sign in."
        })
