from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import TwitterCallbackAPIView, TwitterLoginAPIView


urlpatterns = [
    path("auth/register/", view=RegisterView.as_view(), name="register"),
    path("auth/login/", view=LoginView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/twitter/", TwitterLoginAPIView.as_view(), name="twitter_login"),
    path(
        "twitter/callback/", TwitterCallbackAPIView.as_view(), name="twitter_callback"
    ),
]
