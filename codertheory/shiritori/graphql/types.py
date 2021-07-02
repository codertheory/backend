import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoObjectType, DjangoListField

from .. import models
from ...general import node

__all__ = (
    "ShiritoriGameLobbyType",
    "ShiritoriGameInProgressType",
    "ShiritoriGameType",
    "ShiritoriGameWordType",
    "ShiritoriPlayerType",
)


class ShiritoriGameLobbyType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGame
        interfaces = (node.BaseNode,)
        fields = (
            "id",
            "private",
            "started",
            "finished",
            "shiritoriplayer_set"
        )
        filter_fields = {
            "finished": ['exact'],
            "started": ['exact']
        }


class ShiritoriGameInProgressType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGame
        interfaces = (node.BaseNode,)
        filter_fields = {
            "finished": ['exact'],
            "started": ['exact']
        }


class ShiritoriGameType(graphene.Union):
    class Meta:
        types = (ShiritoriGameLobbyType, ShiritoriGameInProgressType)


class ShiritoriGameWordType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGameWord
        fields = ("id", "word", "created_at")


class ShiritoriPlayerType(DjangoObjectType):
    words = DjangoListField(ShiritoriGameWordType)

    class Meta:
        model = models.ShiritoriPlayer
        fields = "__all__"
        filter_fields = {
            "name": ['exact']
        }

    def resolve_words(self: models.ShiritoriPlayer, info):
        return gql_optimizer.query(models.ShiritoriPlayer.get_words(self.game_id, self.id), info)
