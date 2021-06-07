import time

import channels_graphql_ws
import graphene

from codertheory.shiritori import models
from codertheory.shiritori.graphql.types import ShiritoriGameType


class GameSubscription(channels_graphql_ws.Subscription):
    gameById = graphene.Field(ShiritoriGameType)

    class Arguments:
        id = graphene.ID(description="ID of the game")

    @staticmethod
    def subscribe(root, info, id=None):
        return [id]

    @staticmethod
    def publish(payload, info, id=None):
        time.sleep(0.5)
        return GameSubscription(gameById=models.ShiritoriGame.objects.get(pk=id))
