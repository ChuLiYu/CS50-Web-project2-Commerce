from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Comment, User, Listing, Bidding, Watchlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import (
    ListingModelForm,
    BiddingModelForm,
    WatchListModelForm,
    Listing_ActiveModifyModelForm,
    CommentModelForm,
)
from django.contrib import messages
from django.db.models import Max

# title, description, link, img, strat_bid,  category


def index(request):
    listings_is_active = Listing.objects.filter(is_active=True)
    context = {"listings": listings_is_active, "page_title": "Active Listings"}
    return render(request, "auctions/listings.html", context)


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing_view(request):

    if request.method == "POST":
        # reslove post request to model post for valid
        form = ListingModelForm(request.POST, request.FILES)
        if form.is_valid():
            # create new listing in db
            contact = form.save(commit=False)
            # Set creator as login user
            contact.creator_id = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
    form = ListingModelForm()
    context = {"form": form}
    return render(request, "auctions/create_listing.html", context)


def listing_page_view(request, listing_id):
    # create forms to be rendered
    bidding_form = BiddingModelForm()
    watchlist_form = WatchListModelForm()
    listing_active_modify_form = Listing_ActiveModifyModelForm()
    comment_form = CommentModelForm()

    # check listing in watchlist or not
    try:
        Watchlist.objects.get(creator_id=request.user, listing_id=listing_id)
        is_in_watchlist = True
    except:
        is_in_watchlist = False

    # prepare for new bid to compare the price
    listing = Listing.objects.get(id=listing_id)
    now_price = Bidding.objects.filter(listing_id=listing_id).aggregate(
        Max("bidding_price")
    )["bidding_price__max"]

    # check user is the listing creator or not
    if listing.creator_id == request.user:
        is_now_user_the_creator = True
    else:
        is_now_user_the_creator = False

    # Check user is the listing winner or not
    args = (
        Bidding.objects.filter(listing_id=listing_id).order_by("-bidding_price").first()
    )
    try:
        winner = args.creator_id
    except Exception as e:
        print(f"Error: {e}")
        winner = None
    if winner == request.user:
        is_now_user_the_winner = True
    else:
        is_now_user_the_winner = False

    # for check Listing in Active or not
    is_active = listing.is_active

    comments = Comment.objects.filter(listing_id=listing_id)

    context = {
        "listing": listing,
        "bidding_form": bidding_form,
        "now_price": now_price,
        "watchlist": watchlist_form,
        "is_in_watchlist": is_in_watchlist,
        "listing_active_modify_form": listing_active_modify_form,
        "is_now_user_the_creator": is_now_user_the_creator,
        "is_now_user_the_winner": is_now_user_the_winner,
        "is_active": is_active,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "auctions/listing_page.html", context)


@login_required
def modify_watchlist_view(request, listing_id):

    if not request.method == "POST":
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    add_to_watchlist = request.POST.get("add_to_watchlist")
    remove_from_watchlist = request.POST.get("remove_from_watchlist")
    if not add_to_watchlist and not remove_from_watchlist:
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    is_in_watchlist = False if add_to_watchlist else True

    form = WatchListModelForm(request)
    if form.is_valid():
        if is_in_watchlist:
            Watchlist.objects.get(
                creator_id=request.user, listing_id=listing_id
            ).delete()
        else:
            container = form.save(commit=False)
            container.creator_id = request.user
            container.listing_id = Listing.objects.get(id=listing_id)
            try:
                container.save()
            except IntegrityError:
                # put error message TODO
                return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


@login_required
def watchlist_view(request):
    user = User.objects.get(username=request.user)
    # ManytoMany Realation can use users' objects access Listing directly (without using watchlists' objects).
    user_watchlist = Listing.objects.filter(watchlist_id=user)

    print(user_watchlist)
    context = {
        "Page_title": "My Watchlist",
        "listings": user_watchlist,
    }
    return render(request, "auctions/listings.html", context)


def categories_page_view(request):
    categories = Listing.CATEGORY_CHOICES
    context = {"categories": categories}
    return render(request, "auctions/categories_page.html", context)


def category_page_view(request, category_key):
    context = {
        "listings": Listing.objects.filter(is_active=True, category=category_key),
        "page_title": dict(Listing.CATEGORY_CHOICES)[category_key],
    }
    return render(request, "auctions/listings.html", context)


@login_required
def submit_bid_view(request, listing_id):
    form = BiddingModelForm(request.POST)
    container = form.save(commit=False)

    listing_instance = Listing.objects.get(id=listing_id)
    container.creator_id = request.user
    container.listing_id = listing_instance

    if not (request.method == "POST"):
        return HttpResponseRedirect("listing_page")

    # if request price > existing price and start_bid: then make a new query
    if form.is_valid():

        new_price = int(request.POST.get("bidding_price", ""))

        # get highest bid price for compare
        now_price = Bidding.objects.filter(listing_id=listing_id).aggregate(
            Max("bidding_price")
        )["bidding_price__max"]

        start_bid = Listing.objects.get(id=listing_id).start_bid

        if now_price:
            if new_price > now_price:
                container.biddin_price = new_price
                form.save()
                list(messages.get_messages(request))  # to clean messages

            else:
                messages.error(request, "Price need to higher than existing bid")

        else:
            if new_price > start_bid:
                container.bid_price = new_price
                form.save()
                list(messages.get_messages(request))  # to clean messages

            else:
                messages.error(request, "Price need to higher than start bid")

    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


@login_required
def modify_listing_active_view(request, listing_id):

    if not request.method == "POST":
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    active_listing = request.POST.get("active_listing")
    inactive_listing = request.POST.get("inactive_listing")
    if (not active_listing) and (not inactive_listing):
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    is_active = False if active_listing else True
    listing = Listing.objects.get(pk=listing_id)
    form = Listing_ActiveModifyModelForm(request.POST, instance=listing)
    if form.is_valid():
        container = form.save(commit=False)
        if is_active:
            # change inactive status in Listing
            container.is_acitve = 0
        else:
            container.is_acitve = 1
        container.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

    # put error message TODO


@login_required
def add_comment_view(request, listing_id):
    if not request.method == "POST":
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    if request.POST.get(
        "comment",
    ):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            list = Listing.objects.get(pk=listing_id)
            container.listing_id = list
            container.creator_id = request.user
            container.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


def all_listings_view(request):
    listings_is_active = Listing.objects.all
    context = {"listings": listings_is_active, "page_title": "Active Listings"}
    return render(request, "auctions/listings.html", context)
