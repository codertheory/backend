import graphene
from graphene_django import DjangoObjectType, DjangoListField

from .. import models


class PollVoteType(DjangoObjectType):
    class Meta:
        model = models.PollVote
        fields = ("poll", "option")


class PollOptionType(DjangoObjectType):
    votes = graphene.Int(source="vote_count")

    class Meta:
        model = models.PollOption
        fields = "__all__"


class PollType(DjangoObjectType):
    options = DjangoListField(PollOptionType)
    vote_count = graphene.Int(source="total_vote_count")
    can_vote = graphene.Boolean()

    class Meta:
        model = models.Poll
        fields = "__all__"

    # noinspection PyUnresolvedReferences
    def resolve_can_vote(self, info):
        return models.Poll.can_vote(self.id, info.context.META['REMOTE_ADDR'])
