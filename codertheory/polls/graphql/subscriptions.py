import channels_graphql_ws
import graphene

from codertheory.polls import models
from codertheory.polls.graphql.types import PollType


class PollSubscription(PollType, channels_graphql_ws.Subscription):
    class Meta:
        model = models.Poll
        fields = "__all__"

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
        return PollSubscription(**models.Poll.objects.get(pk=id).to_dict())
