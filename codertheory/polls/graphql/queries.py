import graphene

from . import types
from .. import models


# noinspection PyMethodMayBeStatic
class PollQuery(graphene.ObjectType):
    polls = graphene.List(types.PollType)

    def resolve_polls(self, info):
        return models.Poll.objects.all()
