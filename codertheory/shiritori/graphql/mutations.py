import graphene
from graphql import GraphQLError

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

    game = graphene.Field(types.ShiritoriGameInProgressType)
    player = graphene.Field(types.ShiritoriPlayerType)

    @classmethod
    def mutate(cls, root, info, private=False, player_name=None):
        game = models.ShiritoriGame.objects.create(private=private)
        if player_name:
            player = game.join(game.id, player_name)
        else:
            player = None
        return CreateGameMutation(game=game, player=player)


class JoinGameMutation(graphene.Mutation):
    class Arguments:
        player_name = graphene.String()
        game_id = graphene.ID()

    game = graphene.Field(types.ShiritoriGameLobbyType)
    player = graphene.Field(types.ShiritoriPlayerType)

    @classmethod
    def mutate(cls, root, info, player_name=None, game_id=None):
        player = models.ShiritoriGame.join(game_id, player_name)
        player.game.refresh_from_db()
        return JoinGameMutation(player=player, game=player.game)


class LeaveGameMutation(graphene.Mutation):
    class Arguments:
        player_id = graphene.ID()

    game = graphene.Field(types.ShiritoriGameLobbyType)

    @classmethod
    def mutate(cls, root, info, player_id=None):
        try:
            player = models.ShiritoriPlayer.objects.get(pk=player_id).leave()
            try:
                player.game.refresh_from_db()
            except models.ShiritoriGame.DoesNotExist:
                pass
            return LeaveGameMutation(game=player.game)
        except models.ShiritoriPlayer.DoesNotExist:
            return LeaveGameMutation(None)


class StartGameMutation(graphene.Mutation):
    class Arguments:
        game_id = graphene.ID()
        timer = graphene.Int()

    game = graphene.Field(types.ShiritoriGameInProgressType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, game_id=None, timer=None):
        game = models.ShiritoriGame.objects.get(pk=game_id)
        if timer:
            game.timer = timer
        if game.started:
            raise GraphQLError("Game Already Started")
        try:
            game.start()
        except exceptions.NotEnoughPlayersException as error:
            return StartGameMutation(errors=[str(error)])
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
