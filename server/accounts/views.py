import base64
import hashlib
import os

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tweepy import Client, OAuth2UserHandler
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, RegisterTwitterSerializer
from .utils import get_tokens_for_user

User = get_user_model()


class RegisterView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get(self, request, format=None):
        content = {
            "user": str(request.user),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        # tokens = get_tokens_for_user(serializer)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "user created successfully",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(
            data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, form=None):

        data = request.data

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                data={"user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        tokens = get_tokens_for_user(user)

        return Response(
            data={"message": "Login successful", "tokens": tokens},
            status=status.HTTP_200_OK,
        )


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class TwitterLoginAPIView(APIView):
    """
    Initiates the Twitter OAuth2 login process by generating the authorization URL.
    """

    permission_classes = [AllowAny]

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
        print(request.session.get("code_verifier"))
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

    permission_classes = [AllowAny]
    serializer_class = RegisterTwitterSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve authorization code from query params
        authorization_code = request.query_params.get("code")
        if not authorization_code:
            return Response(data={"error": "Authorization code missing"}, status=400)

        # Retrieve code_verifier from session
        code_verifier = request.session.get("code_verifier")
        print(code_verifier)
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
            refresh_token = response.json()["refresh_token"]
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
            user_id = user_data["data"]["id"]
            username = user_data["data"]["username"]
            data = {
                "username": username,
                "id": user_id,
                "refresh_token": refresh_token,
            }
            try:
                user = get_object_or_404(User, pk=user_id)
                user.refresh_token = refresh_token
                user.save()
            except:
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(user_id=user_id)

            if user is None:
                return Response(
                    data={"user does not exist"}, status=status.HTTP_404_NOT_FOUND
                )
            tokens = get_tokens_for_user(user)
            return Response(
                data={
                    "message": "Twitter authentication successful",
                    "twitter_user": user_data,
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                data={"error": "Failed to fetch access token", "details": str(e)},
                status=500,
            )
