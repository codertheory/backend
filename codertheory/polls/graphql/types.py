from graphene_django import DjangoObjectType, DjangoListField

from .. import models


class PollVoteType(DjangoObjectType):
    class Meta:
        model = models.PollVote
        fields = "__all__"


class PollOptionType(DjangoObjectType):
    class Meta:
        model = models.PollOption
        fields = "__all__"


class PollType(DjangoObjectType):
    options = DjangoListField(PollOptionType)

    class Meta:
        model = models.Poll
        fields = "__all__"
