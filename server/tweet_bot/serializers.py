from rest_framework import serializers
from .models import Tweets
from django.contrib.auth import get_user_model

User = get_user_model()


class TweetsSerializer(serializers.ModelSerializer):
    message = serializers.CharField()
    post_time = serializers.DateTimeField()
    user = User

    class Meta:
        model = Tweets
        fields = "__all__"
