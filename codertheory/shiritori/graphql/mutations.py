from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers

__all__ = (
    "GameMutation",
    "PlayerMutation",
    "GameWordMutation"
)


class GameMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.GameSerializer
        convert_choices_to_enum = False


class PlayerMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PlayerSerializer
        convert_choices_to_enum = False


class GameWordMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.GameWordSerializer
        convert_choices_to_enum = False
