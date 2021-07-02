import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import types
from ...general import node


# noinspection PyMethodMayBeStatic
class GameQuery(graphene.ObjectType):
    games = DjangoFilterConnectionField(types.ShiritoriGameInProgressType)
    game_by_id = node.BaseNode.Field(types.ShiritoriGameType)
