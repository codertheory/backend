import graphene

from .mutations import Mutations
from .query import Query
from .subscriptions import Subscription

__all__ = (
    "Query",
    "Mutations",
    "schema",
    "Subscription"
)

# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutations, subscription=Subscription)
