import graphene
from graphql_auth.schema import UserQuery, MeQuery

from codertheory.polls.graphql.queries import PollQuery
from codertheory.projects.graphql.queries import ProjectQuery
from codertheory.shiritori.graphql.queries import GameQuery

__all__ = (
    "Query",
)


class Query(
    UserQuery,
    MeQuery,
    ProjectQuery,
    GameQuery,
    PollQuery,
    graphene.ObjectType):
    pass
