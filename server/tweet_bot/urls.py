from django.urls import path

from .views import TweetView, DeleteTweetView

# import utils

urlpatterns = [
    path("tweets/", TweetView.as_view(), name="tweets"),
    path("tweets/<str:tweet_id>/", DeleteTweetView.as_view(), name="delete_tweets"),
]
