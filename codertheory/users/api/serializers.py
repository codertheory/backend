from django.contrib.auth import get_user_model
from djoser.serializers import TokenSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "name", "avatar", "role", "date_joined"]
        ref_name = "UserSerializer"


class KnoxTokenSerializer(TokenSerializer):
    auth_token = serializers.CharField(source="token_key")
    expiry = serializers.DateTimeField()

    class Meta(TokenSerializer.Meta):
        fields = ("auth_token", "expiry")
