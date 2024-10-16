# bot/views.py
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tweepy import OAuth2UserHandler


@api_view(["GET"])
def get_authorization_url(request):
    # Initialize the OAuth handler with credentials
    oauth2_user_handler = OAuth2UserHandler(
        client_id="YWNGTjBGM1dlNDY3bDltYUJhQ0s6MTpjaQ",
        redirect_uri="http://127.0.0.1:8000/callback/",
        scope=["tweet.write", "follows.read", "follows.write"],
        client_secret="Gw8RQlwLB5M_PjwrchRcaQNTnpiBjW6AEBV0IEqmwNEABDBtQL",
    )
    try:
        # Generate and return the authorization URL
        authorization_url = oauth2_user_handler.get_authorization_url()
        print("--------------------working -----------------------")

        # Store OAuth2 handler in the session
        request.session["state"] = str(oauth2_user_handler.state)
        print(request.session)
        print("--------------------working -----------------------")
        print(authorization_url)
        return Response({"authorization_url": authorization_url})

    except Exception as e:
        return Response(
            {"error": "Authorization failed", "details": str(e)}, status=400
        )


@api_view(["GET"])
def twitter_callback(request):
    # Retrieve the OAuth handler from session
    state = request.session.get("state", None)

    if not state:
        return Response({"error": "Session expired or invalid."}, status=400)
    # Get the authorization code from the callback URL
    authorization_code = request.GET.get("code")

    if not authorization_code:
        return Response({"error": "Authorization code missing."}, status=400)

    try:
        # Fetch the access token using the authorization code
        oauth2_user_handler = OAuth2UserHandler(
            client_id="YWNGTjBGM1dlNDY3bDltYUJhQ0s6MTpjaQ",
            redirect_uri="http://127.0.0.1:8000/callback/",
            scope=["tweet.write", "follows.read", "follows.write"],
            client_secret="Gw8RQlwLB5M_PjwrchRcaQNTnpiBjW6AEBV0IEqmwNEABDBtQL",
            state=state,
        )
        access_token = oauth2_user_handler.fetch_token(
            token_url="https://api.twitter.com/2/oauth2/token",
            authorization_response=request.build_absolute_uri(),
        )

        # Store the access token in session or database for future use
        request.session["access_token"] = access_token["access_token"]

        return Response(
            {"message": "Access token retrieved", "access_token": access_token}
        )

    except Exception as e:
        return Response(
            {"error": "Failed to fetch access token", "details": str(e)}, status=400
        )
