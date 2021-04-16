import graphene
import graphql_jwt

from codertheory.polls.graphql.mutations import PollMutation, PollVoteMutation
from codertheory.projects.graphql.mutations import ProjectMutation
from codertheory.shiritori.graphql.mutations import *

__all__ = (
    "Mutations",

)


class Mutations(graphene.ObjectType):
    create_project = ProjectMutation.Field()
    create_game = GameWordMutation.Field()
    create_poll = PollMutation.Field()
    vote_poll = PollVoteMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
