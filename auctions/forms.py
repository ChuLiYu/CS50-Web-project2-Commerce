from django import forms
from .models import Comment, Listing, Bidding, Watchlist


class ListingModelForm(forms.ModelForm):
    class Meta:
        model = Listing

        exclude = ["bidding_id", "creator_id", "watchlist_id", "img_link"]


class Listing_ActiveModifyModelForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["is_active"]
        labels = {"is_active": "Active this listing"}


class BiddingModelForm(forms.ModelForm):
    class Meta:
        model = Bidding
        exclude = ["listing_id", "creator_id"]


class WatchListModelForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        exclude = ["creator_id", "listing_id"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_str"]
        labels = {"comment_str": "Comment"}
