import graphene
from channels_graphql_ws.scope_as_context import ScopeAsContext
from django.core.handlers.asgi import ASGIRequest
from graphene import relay
from graphene_django import DjangoObjectType, DjangoListField

from .. import models


class PollVoteType(DjangoObjectType):
    class Meta:
        model = models.PollVote
        fields = ("poll", "option")


class PollOptionType(DjangoObjectType):
    votes = graphene.Int(source="vote_count")
    percentage = graphene.Float(source="vote_percentage")

    class Meta:
        model = models.PollOption
        fields = "__all__"
        interfaces = (relay.Node,)


class PollType(DjangoObjectType):
    options = DjangoListField(PollOptionType)
    vote_count = graphene.Int(source="total_vote_count")
    can_vote = graphene.Boolean()

    class Meta:
        model = models.Poll
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            "active": ['exact']
        }
        interfaces = (relay.Node,)
        fields = "__all__"

    # noinspection PyUnresolvedReferences
    def resolve_can_vote(self, info):
        ip = None
        if isinstance(info.context, ScopeAsContext):
            # noinspection PyProtectedMember
            ip = info.context._scope['client'][0]
        elif isinstance(info.context, ASGIRequest):
            ip = info.context.META['REMOTE_ADDR']
        return models.Poll.can_vote(self.id, ip)
