import graphene
from django.core.exceptions import BadRequest
from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers, types
from .. import models

__all__ = (
    "PollOptionMutation",
    "PollMutation",
    "CreatePollMutation",
    "PollVoteMutation"
)


class PollOptionMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PollOptionSerializer
        convert_choices_to_enum = False


class PollMutation(SerializerMutation):
    options = graphene.List(types.PollOptionType)

    class Meta:
        serializer_class = serializers.PollSerializer
        convert_choices_to_enum = False


class PollOptionInput(graphene.InputObjectType):
    option = graphene.String()


class CreatePollMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        options = graphene.List(PollOptionInput, required=True)
        description = graphene.String()

    poll = graphene.Field(types.PollType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        options = kwargs.get('options')
        if options:
            if len(set([option['option'] for option in options])) < len(options):
                raise BadRequest("Options Must be Unique")
        instance = serializers.PollSerializer(data=kwargs)
        if instance.is_valid(raise_exception=True):
            poll = instance.save()
            # noinspection PyArgumentList
            return CreatePollMutation(poll=poll)


class PollVoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="Poll Option ID")

    option = graphene.Field(types.PollOptionType)

    @classmethod
    def mutate(cls, root, info, id=None):
        poll_option = models.PollOption.objects.get(pk=id)
        poll_option.vote()
        # noinspection PyArgumentList
        return PollVoteMutation(option=poll_option)
