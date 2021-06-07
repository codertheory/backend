import graphene

from . import types
from .. import models

__all__ = (
    "CreateGameMutation",
    "LeaveGameMutation",
    "TakeTurnMutation"
)


class CreateGameMutation(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=False, deprecation_reason=False)

    game = graphene.Field(types.ShiritoriGameType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        return CreateGameMutation(models.ShiritoriGame.objects.create(**input))


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
