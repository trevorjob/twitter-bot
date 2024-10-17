# Importing Tweepy
import tweepy
from harlanapi import settings
from tweepy.errors import *
import requests
from pytwitter import Api

# Credentials
api_key = settings.X_API_KEY
api_secret = settings.X_API_SECRET
bearer_token = settings.X_BEARER_TOKEN
access_token = settings.X_ACCESS_TOKEN
access_token_secret = settings.X_ACCESS_TOKEN_SECRET

# Gainaing access and connecting to Twitter API using Credentials
# client = tweepy.Client(
#     bearer_token, api_key, api_secret, access_token, access_token_secret
# )
# auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
# api = tweepy.API(auth)


# client.follow_user
def create_tweet(message: str, bearer_token: str):
    api = Api(bearer_token=bearer_token)
    ddd = api.create_tweet(text=message)
