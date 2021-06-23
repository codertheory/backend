import graphene

__all__ = (
    "Subscription"
)

from codertheory.polls.graphql.subscriptions import PollSubscription
from codertheory.shiritori.graphql.subscriptions import GameSubscription


class Subscription(graphene.ObjectType):
    poll_subscription = PollSubscription.Field()
    game_subscription = GameSubscription.Field()
