import asyncio
import typing

import channels_graphql_ws
import graphene
from channels.db import database_sync_to_async

from codertheory.polls import models
from codertheory.polls.graphql.types import PollType


class PollSubscription(channels_graphql_ws.Subscription):
    pollById = graphene.Field(PollType)

    class Arguments:
        id = graphene.ID(description="ID of the Poll")

    @staticmethod
    async def subscribe(root, info, id=None):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        return [id]

    @staticmethod
    @database_sync_to_async
    def get_poll(id) -> typing.Awaitable[models.Poll]:
        return models.Poll.objects.get(pk=id)

    @staticmethod
    async def publish(payload, info, id):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `PollSubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        await asyncio.sleep(0.5)  # TODO figure out why there is a race condition with the DB
        poll = await PollSubscription.get_poll(id)
        return PollSubscription(pollById=poll)
