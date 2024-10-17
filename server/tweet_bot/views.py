from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Tweets
from .serializers import TweetsSerializer
from .utils import create_tweet

# Create your views here.


class TweetView(APIView):
    serializer_class = TweetsSerializer
    query_set = Tweets.objects.all()
    # permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        tweets = Tweets.objects.all()

        serializer = self.serializer_class(instance=tweets, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        print(request.session.get("x_access_token"))
        twitter_access_token = request.session.get("x_access_token")
        if not twitter_access_token:
            return Response(
                data={"error": "missing access token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            create_tweet(data.get("message"), twitter_access_token)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            data={"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteTweetView(APIView):

    def delete(self, request: Request, tweet_id: str):
        # return self.destroy(request, pk)
        tweet = get_object_or_404(Tweets, pk=tweet_id)
        tweet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
