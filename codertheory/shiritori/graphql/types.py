from graphene_django import DjangoObjectType

from .. import models
from ...general import node

__all__ = (
    "ShiritoriGameType",
    "ShiritoriPlayerType"
)


class ShiritoriGameType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGame
        exclude = ('password',)
        interfaces = (node.BaseNode,)
        filter_fields = {
            "finished": ['exact'],
            "started": ['exact']
        }


class ShiritoriPlayerType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriPlayer
        fields = "__all__"
        interfaces = (node.BaseNode,)
        filter_fields = {
            "name": ['exact']
        }
