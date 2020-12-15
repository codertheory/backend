from graphene_django import DjangoObjectType
from pinax.blog import models


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post
        fields = "__all__"
