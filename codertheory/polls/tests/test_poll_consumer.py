import typing

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from config.websocket import router
from . import factories


class PollConsumerTests(TransactionTestCase):
    serialized_rollback = False

    @database_sync_to_async
    def _create_poll(self) -> typing.Awaitable[factories.models.Poll]:
        poll = factories.PollFactory()
        factories.PollOptionFactory.create_batch(2, poll=poll)
        return poll

    @database_sync_to_async
    def _vote(self, poll):
        poll.options[0].vote()

    async def test_poll_vote_events(self):
        poll = await self._create_poll()
        communicator = WebsocketCommunicator(router, f"ws/polls/{poll.id}")
        connected, subprotocol = await communicator.connect()
        payload = await communicator.receive_json_from()
        self.assertEqual(payload['type'], "connect")
        self.assertTrue(connected)
        await self._vote(poll)
        payload = await communicator.receive_json_from()
        self.assertEqual(payload['type'], 'pollVote')
