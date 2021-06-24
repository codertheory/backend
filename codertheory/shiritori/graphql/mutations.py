import graphene

from codertheory.shiritori import exceptions
from . import types
from .. import models

__all__ = (
    "CreateGameMutation",
    "JoinGameMutation",
    "LeaveGameMutation",
    "StartGameMutation",
    "TakeTurnMutation"
)


class CreateGameMutation(graphene.Mutation):
    class Arguments:
        private = graphene.Boolean()

    game = graphene.Field(types.ShiritoriGameType)

    @classmethod
    def mutate(cls, root, info, private=False):
        return CreateGameMutation(models.ShiritoriGame.objects.create(private=private))


class JoinGameMutation(graphene.Mutation):
    class Arguments:
        player_name = graphene.String()
        game_id = graphene.ID()

    player = graphene.Field(types.ShiritoriPlayerType)

    @classmethod
    def mutate(cls, root, info, player_name=None, game_id=None):
        game = models.ShiritoriGame.objects.get(pk=game_id)
        player = game.join(player_name)
        return JoinGameMutation(player=player)


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
            return LeaveGameMutation(game=game)
        except:
            return


class StartGameMutation(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        timer = graphene.Int()

    game = graphene.Field(types.ShiritoriGameType)

    @classmethod
    def mutate(cls, root, info, game_id=None, timer=None):
        game = models.ShiritoriGame.objects.get(pk=game_id)
        game.timer = timer
        try:
            game.start()
        except exceptions.NotEnoughPlayersException as error:
            raise Exception(str(error))
        return StartGameMutation(game=game)


class TakeTurnMutation(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        word = graphene.String()

    score = graphene.Int()

    @classmethod
    def mutate(cls, root, info, word=None, game_id=None):
        game = models.ShiritoriGame.objects.get(pk=game_id)
        game.take_turn(word)
