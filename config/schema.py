import graphene

from codertheory.blog.graphql.mutations import PostMutation
from codertheory.blog.graphql.queries import ArticleQuery
from codertheory.projects.graphql.mutations import ProjectMutation
from codertheory.projects.graphql.queries import ProjectQuery
from codertheory.users.graphql.query import UserQuery


# noinspection PyMethodMayBeStatic
class Query(
    UserQuery,
    ArticleQuery,
    ProjectQuery,
    graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    create_post = PostMutation.Field()
    create_project = ProjectMutation.Field()


# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutations)
