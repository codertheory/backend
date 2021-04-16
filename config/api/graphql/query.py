import graphene

from codertheory.polls.graphql.queries import PollQuery
from codertheory.projects.graphql.queries import ProjectQuery
from codertheory.shiritori.graphql.queries import GameQuery
from codertheory.users.graphql.query import UserQuery

__all__ = (
    "Query",
)


class Query(
    UserQuery,
    ProjectQuery,
    GameQuery,
    PollQuery,
    graphene.ObjectType):
    pass
