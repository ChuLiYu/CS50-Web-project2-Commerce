from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing_page/<int:listing_id>", views.listing_page_view, name="listing_page"),
    path(
        "listing_page/<int:listing_id>/sumbit_bid",
        views.submit_bid_view,
        name="submit_bid",
    ),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path(
        "listing_page/<int:listing_id>/modify_watchlist",
        views.modify_watchlist_view,
        name="modify_watchlist",
    ),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("categories_page", views.categories_page_view, name="categories_page"),
    path(
        "category_page/<str:category_key>", views.category_page_view, name="category_page"
    ),
    path(
        "listing_page/<int:listing_id>/modify_listing_active",
        views.modify_listing_active_view,
        name="modify_listing_active",
    ),
    path(
        "listing_page/<int:listing_id>/add_comment",
        views.add_comment_view,
        name="add_comment",
    ),
]
