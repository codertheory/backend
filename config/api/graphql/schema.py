import graphene

from .mutations import Mutations
from .query import Query

__all__ = (
    "Query",
    "Mutations",
    "schema"
)

# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutations)
