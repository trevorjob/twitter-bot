from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from .utils import get_tokens_for_user


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
