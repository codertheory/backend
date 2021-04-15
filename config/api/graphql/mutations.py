import graphene
import graphql_jwt

from codertheory.projects.graphql.mutations import ProjectMutation

__all__ = (
    "Mutations",

)


class Mutations(graphene.ObjectType):
    create_project = ProjectMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
