import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers, types
from .. import models


class PollOptionMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PollOptionSerializer
        convert_choices_to_enum = False


class PollMutation(SerializerMutation):
    options = PollOptionMutation.Field()

    class Meta:
        serializer_class = serializers.PollSerializer
        convert_choices_to_enum = False


class PollVoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="Poll Option ID")

    option = graphene.Field(types.PollOptionType)

    @classmethod
    def mutate(cls, root, info, text=None, id=None):
        poll_option = models.PollOption.objects.get(pk=id)
        poll_option.vote()
        # noinspection PyArgumentList
        return PollVoteMutation(option=poll_option)
