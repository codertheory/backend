from rest_framework import serializers

from codertheory.shiritori import models

__all__ = (
    "GameSerializer",
    "PlayerSerializer",
    "GameWordSerializer",
)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiritoriPlayer
        fields = ("id","name", "score", "lives")


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = models.ShiritoriGame
        exclude = ("password",)


class GameWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShiritoriGameWord
        fields = "__all__"
