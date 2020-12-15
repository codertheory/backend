import graphene

from codertheory.users import models
from codertheory.users.graphql import types


# noinspection PyMethodMayBeStatic
class UserQuery(graphene.ObjectType):
    users = graphene.List(types.UserType)

    def resolve_users(self, info):
        return models.User.objects.all()
