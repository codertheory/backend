import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import types
from ...general import node


class PollQuery(graphene.ObjectType):
    polls = DjangoFilterConnectionField(types.PollType)
    poll_by_id = node.BaseNode.Field(types.PollType)
