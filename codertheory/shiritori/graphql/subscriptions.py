import asyncio
import typing

import channels_graphql_ws
import graphene
from channels.db import database_sync_to_async

from codertheory.shiritori import models
from codertheory.shiritori.graphql.types import ShiritoriGameType


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
