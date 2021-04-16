from graphene_django import DjangoObjectType

from .. import models


class ShiritoriGameType(DjangoObjectType):
    class Meta:
        model = models.ShiritoriGame
        exclude = ('password',)
