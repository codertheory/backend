from graphene_django import DjangoObjectType

from .. import models


class PollType(DjangoObjectType):
    class Meta:
        model = models.Poll
        fields = "__all__"
