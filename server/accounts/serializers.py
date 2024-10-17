from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RegisterTwitterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    id = serializers.CharField(max_length=50)
    refresh_token = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["id", "username", "refresh_token"]

