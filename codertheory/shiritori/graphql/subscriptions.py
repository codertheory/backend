import asyncio
import typing

import channels_graphql_ws
import graphene
import graphene_django_optimizer as gql_optimizer
from channels.db import database_sync_to_async
from graphene_django import DjangoListField

from codertheory.shiritori import models
from codertheory.shiritori.graphql.types import ShiritoriGameType, ShiritoriPlayerType

__all__ = (
    "GameSubscription",
    "PlayerSubscription"
)


class GameSubscription(channels_graphql_ws.Subscription):
    gameById = graphene.Field(ShiritoriGameType)

    class Arguments:
        game_id = graphene.ID(description="ID of the game")

    @staticmethod
    def subscribe(root, info, game_id=None):
        return [game_id]

    @staticmethod
    @database_sync_to_async
    def get_game(game_id) -> typing.Awaitable[models.ShiritoriGame]:
        return models.ShiritoriGame.objects.get(pk=game_id)

    @staticmethod
    async def publish(payload, info, game_id=None):
        await asyncio.sleep(0.5)
        game = await GameSubscription.get_game(game_id)
        return GameSubscription(gameById=game)


class PlayerSubscription(channels_graphql_ws.Subscription):
    players = DjangoListField(ShiritoriPlayerType)

    class Arguments:
        game_id = graphene.ID(description="ID of the game")

    @staticmethod
    @database_sync_to_async
    def get_players(info, game_id) -> typing.Awaitable[models.QuerySet[models.ShiritoriPlayer]]:
        return gql_optimizer.query(models.ShiritoriPlayer.objects.filter(game__id=game_id), info)

    @staticmethod
    async def publish(payload, info, game_id=None):
        await asyncio.sleep(0.5)
        players = await PlayerSubscription.get_players(info, game_id)
        return PlayerSubscription(players=players)
