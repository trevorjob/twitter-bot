# Importing Tweepy
import tweepy
from harlanapi import settings
from tweepy.errors import *

# Credentials
api_key = settings.X_API_KEY
api_secret = settings.X_API_SECRET
bearer_token = settings.X_BEARER_TOKEN
access_token = settings.X_ACCESS_TOKEN
access_token_secret = settings.X_ACCESS_TOKEN_SECRET

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(
    bearer_token, api_key, api_secret, access_token, access_token_secret
)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)


def create_tweet():
    try:
        client.create_tweet(text="Hello World")
        return True
    except:
        return None
