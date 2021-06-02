import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from . import types


class PollQuery(graphene.ObjectType):
    polls = DjangoFilterConnectionField(types.PollType)
    poll_by_id = relay.Node.Field(types.PollType)
