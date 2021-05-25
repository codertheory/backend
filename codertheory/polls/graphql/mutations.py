import graphene
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from graphene_django.rest_framework.mutation import SerializerMutation
from graphql.error import GraphQLLocatedError

from . import serializers, types
from .. import models

__all__ = (
    "PollOptionMutation",
    "PollMutation",
    "PollOptionInput",
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
        description = graphene.String(required=False)

    poll = graphene.Field(types.PollType)

    @classmethod
    def mutate(cls, root, info, name=None, options=None, description=None):
        if options:
            if len(set(option['option'] for option in options)) < len(options):
                raise BadRequest("Options Must be Unique")
            if len(options) == 1:
                raise BadRequest("Polls Must have more than 1 option")
        instance = serializers.PollSerializer(data=dict(
            name=name, options=options, description=description
        ))
        if instance.is_valid():
            poll = instance.save()
            # noinspection PyArgumentList
            return CreatePollMutation(poll=poll)
        else:
            raise BadRequest(instance.errors)


class PollVoteMutation(graphene.Mutation):
    class Arguments:
        poll_id = graphene.ID(description="Poll ID")
        option_id = graphene.ID(description="Poll Option ID")

    vote = graphene.Field(types.PollVoteType)

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    @classmethod
    def mutate(cls, root, info, poll_id=None, option_id=None):
        try:
            vote = models.PollVote.vote(poll_id, option_id, info.context.META['REMOTE_ADDR'])
            return PollVoteMutation(vote=vote)
        except (IntegrityError, GraphQLLocatedError) as error:
            if isinstance(error, IntegrityError):
                for arg in error.args:
                    if 'unique constraint' in arg.lower():
                        raise Exception("IP Already Voted") from error
            raise error from error
