import graphene

from codertheory.projects.graphql.mutations import ProjectMutation

__all__ = (
    "Mutations",

)


class Mutations(graphene.ObjectType):
    create_project = ProjectMutation.Field()
