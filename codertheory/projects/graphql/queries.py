import graphene

from . import types
from .. import models


# noinspection PyMethodMayBeStatic
class ProjectQuery(graphene.ObjectType):
    projects = graphene.List(types.ProjectType)

    def resolve_projects(self, info):
        return models.Project.objects.all()
