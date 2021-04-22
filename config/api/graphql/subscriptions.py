import graphene

__all__ = (
    "Subscription"
)

from codertheory.polls.graphql.subscriptions import PollSubscription


class Subscription(graphene.ObjectType):
    poll_subscription = PollSubscription.Field()
