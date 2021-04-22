import channels_graphql_ws
import graphene

from codertheory.polls import models
from codertheory.polls.graphql.types import PollType


class PollSubscription(channels_graphql_ws.Subscription):
    # Subscription payload.
    event = graphene.String()
    poll = graphene.Field(PollType)

    class Arguments:
        id = graphene.ID(description="ID of the Poll")

    @staticmethod
    def subscribe(root, info, id=None):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        try:
            return [id]
        finally:
            PollSubscription.broadcast(group=id, payload={
                "poll": models.Poll.objects.get(pk=id)
            })

    @staticmethod
    def publish(payload, info, id):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `PollSubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        return PollSubscription(event="Yolo", poll=models.Poll.objects.get(pk=id))
