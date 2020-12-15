from graphene_django import DjangoObjectType

from .. import models


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project
        fields = "__all__"
