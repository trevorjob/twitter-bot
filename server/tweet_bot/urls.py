from django.urls import path
from .views import TweetView

# import utils

urlpatterns = [path("tweet/", TweetView.as_view(), name="tweets")]
