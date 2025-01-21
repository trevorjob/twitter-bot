import requests
from harlanapi import settings
from pytwitter import Api
from pytwitter.error import *
from .models import Tweets

# Credentials
api_key = settings.X_API_KEY
api_secret = settings.X_API_SECRET
bearer_token = settings.X_BEARER_TOKEN
access_token = settings.X_ACCESS_TOKEN
access_token_secret = settings.X_ACCESS_TOKEN_SECRET


def create_tweet(message: str, bearer_token: str):
    try:
        api = Api(bearer_token=bearer_token)
        tweet = api.create_tweet(text=message)
        return tweet
    except PyTwitterError:
        return None


def get_access_token(refresh_token: str):
    token_url = "https://api.twitter.com/2/oauth2/token"
    refresh_token = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": settings.X_CLIENT_ID,
    }
    response = requests.post(
        token_url,
        data=refresh_token,
        auth=(settings.X_CLIENT_ID, settings.X_CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()
