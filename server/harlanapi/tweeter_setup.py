# bot/views.py
from django.shortcuts import render, redirect
from tweepy import OAuth2UserHandler, Client
import os
from rest_framework.response import Response
from rest_framework import status


def authorize(request):
    oauth2_user_handler = OAuth2UserHandler(
        client_id="YWNGTjBGM1dlNDY3bDltYUJhQ0s6MTpjaQ",
        redirect_uri="http://127.0.0.1:8000/callback/",
        scope=["tweet.write", "follows.read", "follows.write"],
        client_secret="Gw8RQlwLB5M_PjwrchRcaQNTnpiBjW6AEBV0IEqmwNEABDBtQL",
    )
    authorization_url = oauth2_user_handler.get_authorization_url()
    request.session["oauth2_user_handler"] = oauth2_user_handler
    return Response(data={"url": authorization_url}, status=status.HTTP_200_OK)


def callback(request):
    oauth2_user_handler = request.session.get("oauth2_user_handler", None)
    if oauth2_user_handler:
        authorization_code = request.GET.get("code")
        access_token = oauth2_user_handler.fetch_token(
            token_url="https://api.twitter.com/2/oauth2/token",
            authorization_response=request.build_absolute_uri(),
        )
        request.session["access_token"] = access_token["access_token"]
        return redirect("dashboard")  # Redirect to your dashboard view

    return redirect("authorize")
