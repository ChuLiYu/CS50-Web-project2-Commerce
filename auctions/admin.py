from django.contrib import admin
from .models import User, Listing, Watchlist, Bidding, Comment

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "img", "category")


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(Watchlist)
