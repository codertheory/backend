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
        player_name = graphene.String()

    game = graphene.Field(types.ShiritoriGameType)
    player = graphene.Field(types.ShiritoriPlayerType)

    @classmethod
    def mutate(cls, root, info, private=False, player_name=None):
        game = models.ShiritoriGame.objects.create(private=private)
        if player_name:
            player = game.join(player_name)
        else:
            player = None
        return CreateGameMutation(game=game, player=player)


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
            player = models.ShiritoriPlayer.objects.get(pk=player_id, game__id=game_id).leave()
            return LeaveGameMutation(game=player.game)
        except models.ShiritoriPlayer.DoesNotExist:
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
