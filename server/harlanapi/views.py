# bot/views.py

import base64
import hashlib
import os

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tweepy import Client, OAuth2UserHandler
import requests

# from .utils import *

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class TwitterLoginAPIView(APIView):
    """
    Initiates the Twitter OAuth2 login process by generating the authorization URL.
    """

    @staticmethod
    def generate_code_verifier():
        # Generate a cryptographically random code_verifier
        code_verifier = (
            base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
        )
        return code_verifier

    @staticmethod
    def generate_code_challenge(code_verifier):
        # Generate a code_challenge from the code_verifier
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = (
            base64.urlsafe_b64encode(code_challenge).decode("utf-8").rstrip("=")
        )
        return code_challenge

    def get(self, request, *args, **kwargs):
        random_state = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")

        # Store state in session
        request.session["oauth_state"] = random_state
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)

        # Store the code_verifier in session
        request.session["code_verifier"] = code_verifier
        try:
            # Construct authorization URL
            authorization_url = (
                f"https://twitter.com/i/oauth2/authorize"
                f"?response_type=code"
                f"&client_id={settings.X_CLIENT_ID}"
                f"&redirect_uri={settings.X_REDIRECT_URI}"
                f"&scope={' '.join(settings.X_SCOPES)}"
                f"&state={random_state}"
                f"&code_challenge={code_challenge}"
                f"&code_challenge_method=S256"
            )
            return Response(
                {"authorization_url": authorization_url}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Failed to generate authorization URL", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TwitterCallbackAPIView(APIView):
    """
    Handles the callback from Twitter after user authorization.
    Exchanges the authorization code for an access token.
    """

    def get(self, request, *args, **kwargs):
        # Retrieve authorization code from query params
        authorization_code = request.query_params.get("code")
        if not authorization_code:
            return Response(data={"error": "Authorization code missing"}, status=400)

        # Retrieve code_verifier from session
        code_verifier = request.session.get("code_verifier")
        if not code_verifier:
            return Response(
                data={"error": "Session expired or code_verifier missing"}, status=400
            )

        try:
            # Exchange authorization code for access token
            token_url = "https://api.twitter.com/2/oauth2/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": settings.X_CLIENT_ID,
                "redirect_uri": settings.X_REDIRECT_URI,
                "code_verifier": code_verifier,
                "code": authorization_code,
            }

            response = requests.post(
                token_url,
                data=data,
                auth=(settings.X_CLIENT_ID, settings.X_CLIENT_SECRET),
            )

            if response.status_code != 200:
                return Response(
                    data={
                        "error": "Failed to fetch access token",
                        "details": response.json(),
                    },
                    status=500,
                )

            access_token = response.json()["access_token"]

            # Fetch user info using access token
            headers = {
                "Authorization": f"Bearer {access_token}",
            }
            user_response = requests.get(
                "https://api.twitter.com/2/users/me", headers=headers
            )
            if user_response.status_code != 200:
                return Response(
                    data={
                        "error": "Failed to fetch user info",
                        "details": user_response.json(),
                    },
                    status=500,
                )

            user_data = user_response.json()
            request.session["x_access_token"] = access_token
            request.session["x_user_id"] = user_data["data"]["id"]
            request.session["x_username"] = user_data["data"]["username"]
            return Response(
                data={
                    "message": "Twitter authentication successful",
                    "twitter_user": user_data,
                },
                status=200,
            )

        except Exception as e:
            return Response(
                data={"error": "Failed to fetch access token", "details": str(e)},
                status=500,
            )
