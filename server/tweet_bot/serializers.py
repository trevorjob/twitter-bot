from rest_framework import serializers
from .models import Tweets


class TweetsSerializer(serializers.ModelSerializer):
    message = serializers.CharField()
    post_time = serializers.DateTimeField()

    class Meta:
        model = Tweets
        fields = "__all__"
