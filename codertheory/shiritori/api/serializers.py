from rest_framework import serializers

from codertheory.shiritori import models

__all__ = (
    "GameSerializer",
    "PlayerSerializer",
    "GameWordSerializer",
)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiritoriGame
        exclude = ("password",)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiritoriPlayer
        fields = "__all__"


class GameWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiritoriGameWord
        fields = "__all__"
