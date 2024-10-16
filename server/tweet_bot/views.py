from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .utils import create_tweet
from rest_framework import status

# Create your views here.


class TweetView(APIView):

    def post(self, request: Request):
        res = create_tweet()

        if res is None:
            return Response(
                data={"status": "error"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data={"status": "success"}, status=status.HTTP_200_OK)
