import graphene

from . import types
from .. import models


# noinspection PyMethodMayBeStatic
class PollQuery(graphene.ObjectType):
    polls = graphene.List(types.PollType)

    def resolve_polls(self, info):
        return models.Poll.objects.all()

    poll_by_id = graphene.Field(types.PollType, id=graphene.ID())

    def resolve_poll_by_id(self, info, id):
        try:
            return models.Poll.objects.get(pk=id)
        except models.Poll.DoesNotExist:
            return None

    poll_exists = graphene.Field(graphene.Boolean, id=graphene.ID())

    def resolve_poll_exists(self, info, id=None):
        return models.Poll.objects.filter(pk=id).exists()
