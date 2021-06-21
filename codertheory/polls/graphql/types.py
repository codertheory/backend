import typing

import graphene
from channels_graphql_ws.scope_as_context import ScopeAsContext
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from graphene_django import DjangoObjectType, DjangoListField

from codertheory.general import node
from .. import models


def get_ip(info) -> typing.Optional[str]:
    ip = None
    if isinstance(info.context, ScopeAsContext):
        # noinspection PyProtectedMember
        ip = info.context._scope['client'][0]
    elif isinstance(info.context, (ASGIRequest, WSGIRequest)):
        ip = info.context.META['REMOTE_ADDR']
    return ip


class PollVoteType(DjangoObjectType):
    class Meta:
        model = models.PollVote
        fields = "__all__"


class PollOptionType(DjangoObjectType):
    votes = graphene.Int(source="vote_count")
    percentage = graphene.Float(source="vote_percentage")

    class Meta:
        model = models.PollOption
        fields = "__all__"
        interfaces = (node.BaseNode,)


class PollType(DjangoObjectType):
    options = DjangoListField(PollOptionType)
    vote_count = graphene.Int(source="total_vote_count")
    can_vote = graphene.Boolean()
    vote = graphene.Field(PollVoteType, description="The Clients Vote, if one exists")

    class Meta:
        model = models.Poll
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            "active": ['exact']
        }
        interfaces = (node.BaseNode,)
        fields = "__all__"

    # noinspection PyUnresolvedReferences
    def resolve_can_vote(self, info):
        ip = get_ip(info)
        return models.Poll.can_vote(self.id, ip)

    # noinspection PyUnresolvedReferences
    def resolve_vote(self, info):
        ip = get_ip(info)
        try:
            return models.PollVote.objects.get(poll_id=self.id, ip=ip)
        except models.PollVote.DoesNotExist:
            return None
