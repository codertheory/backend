import graphene

from codertheory.polls.graphql.mutations import *
from codertheory.projects.graphql.mutations import *
from codertheory.shiritori.graphql.mutations import *

__all__ = (
    "Mutations",
)


class Mutations(graphene.ObjectType):
    create_project = ProjectMutation.Field()
    create_game = CreateGameMutation.Field()
    leave_game = LeaveGameMutation.Field()
    take_turn = TakeTurnMutation.Field()
    create_poll = CreatePollMutation.Field()
    vote_poll = PollVoteMutation.Field()
