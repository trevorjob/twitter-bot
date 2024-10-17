from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class UserIDBackend(BaseBackend):
    """
    Custom backend to authenticate users using user_id and password.
    """

    def authenticate(self, request, user_id=None, password=None, **kwargs):
        User = get_user_model()  # Get the user model
        try:
            # Try to fetch the user by ID
            user = User.objects.get(id=user_id)
            # Check if the password is correct
            return user
        except User.DoesNotExist:
            # Return None if the user does not exist or password is incorrect
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
