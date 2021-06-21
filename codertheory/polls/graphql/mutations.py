import sys
import traceback

import graphene
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from graphql.error import GraphQLLocatedError

from . import serializers, types
from .. import models

__all__ = (
    "PollOptionInput",
    "CreatePollMutation",
    "PollVoteMutation",
    "ClearVoteMutation"
)


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
        vote_id = graphene.ID(required=False, description="The ID of the Vote, used for changing a vote")

    vote = graphene.Field(types.PollVoteType)

    @classmethod
    def mutate(cls, root, info, poll_id=None, option_id=None, vote_id=None):
        try:
            ip = types.get_ip(info)
            vote = models.PollVote.vote(poll_id, option_id, ip, vote_id)
            return PollVoteMutation(vote=vote)
        except (IntegrityError, GraphQLLocatedError) as error:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            if isinstance(error, IntegrityError):
                for arg in error.args:
                    if 'unique constraint' in arg.lower():
                        raise Exception("IP Already Voted") from error
            raise error from error


class ClearVoteMutation(graphene.Mutation):
    class Arguments:
        vote_id = graphene.ID()

    success = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, vote_id=None):
        ip = types.get_ip(info)
        try:
            models.PollVote.clear(vote_id, ip)
            return ClearVoteMutation(success=True)
        except Exception as error:
            return ClearVoteMutation(success=False, message=str(error))
