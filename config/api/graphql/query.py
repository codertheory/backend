import graphene

from codertheory.projects.graphql.queries import ProjectQuery
from codertheory.users.graphql.query import UserQuery

__all__ = (
    "Query",
)


class Query(
    UserQuery,
    ProjectQuery,
    graphene.ObjectType):
    pass
