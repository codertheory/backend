from rest_framework import serializers

from codertheory.shiritori import models

__all__ = (
    "GameSerializer",
    "PlayerSerializer",
    "GameWordSerializer",
)


class GameWordSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.ShiritoriGameWord
        fields = ("word", "score")


class PlayerSerializer(serializers.ModelSerializer):
    words = GameWordSerializer(many=True, read_only=True)
    is_current = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.ShiritoriPlayer
        fields = ("id", "name", "score", "words","is_current")


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    host = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.ShiritoriGame
        exclude = ("password",)
