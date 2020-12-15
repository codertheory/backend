import graphene
from pinax.blog.models import Post

from . import types


# noinspection PyMethodMayBeStatic
class ArticleQuery(graphene.ObjectType):
    articles = graphene.List(types.PostType)

    def resolve_articles(self, info):
        return Post.objects.published()
