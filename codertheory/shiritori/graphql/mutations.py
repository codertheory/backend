import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers, types
from .. import models

__all__ = (
    "GameMutation",
    "PlayerMutation",
    "GameWordMutation",
    "LeaveGameMutation",
    "TakeTurnMutation"
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


class LeaveGameMutation(graphene.Mutation):
    class Arguments:
        player_id = graphene.ID()
        game_id = graphene.ID()

    game = graphene.Field(types.ShiritoriGameType)

    @classmethod
    def mutate(cls, root, info, player_id=None, game_id=None):
        try:
            game = models.ShiritoriPlayer.objects.get(pk=game_id)
            game.leave(player_id)
        except:
            return


class TakeTurnMutation(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        word = graphene.String()

    score = graphene.Int()

    @classmethod
    def mutate(cls, root, info, word=None, game_id=None):
        pass
