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
        poll_id = graphene.ID(description="Poll ID")
        option_id = graphene.ID(description="Poll Option ID")

    vote = graphene.Field(types.PollVoteType)

    @classmethod
    def mutate(cls, root, info, poll_id=None, option_id=None):
        try:
            vote = models.PollVote.vote(poll_id, option_id, info.context.META['REMOTE_ADDR'])
        except (IntegrityError, GraphQLLocatedError) as error:
            if isinstance(error, IntegrityError):
                for arg in error.args:
                    if 'unique constraint' in arg.lower():
                        raise Exception("IP Already Voted")
                else:
                    raise
            else:
                raise
        # noinspection PyArgumentList
        return PollVoteMutation(vote=vote)
