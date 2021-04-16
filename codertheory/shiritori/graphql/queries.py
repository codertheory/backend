import graphene

from . import types
from .. import models


# noinspection PyMethodMayBeStatic
class GameQuery(graphene.ObjectType):
    games = graphene.List(types.ShiritoriGameType)

    def resolve_games(self, info):
        return models.ShiritoriGame.objects.all()
