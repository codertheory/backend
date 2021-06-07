from graphene_django import DjangoObjectType

from .. import models
from ...general import node


class ShiritoriGameType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGame
        exclude = ('password',)
        interfaces = (node.BaseNode,)
        filter_fields = {
            "finished": ['exact'],
            "started": ['exact']
        }
