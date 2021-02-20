import typing

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from codertheory.shiritori.events import ShiritoriEvents
from codertheory.shiritori.models import *
from codertheory.shiritori.tests.factories import *
from config.websocket import router


class TimerConsumerTests(TransactionTestCase):
    serialized_rollback = False

    @database_sync_to_async
    def _create_game(self) -> typing.Awaitable[ShiritoriGame]:
        return GameFactory(timer=3)

    @database_sync_to_async
    def _start_game(self, g):
        g.started = True
        g.save()

    async def _setup(self) -> typing.Tuple[WebsocketCommunicator, ShiritoriGame]:
        game = await self._create_game()
        communicator = WebsocketCommunicator(router, f"ws/shiritori/game/{game.id}/timer")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_json_from()
        return communicator, game

    async def test_countdown(self):
        communicator, game = await self._setup()
        await self._start_game(game)
        counts = []
        while True:
            data = await communicator.receive_json_from(timeout=1.2)
            if data['type'] == ShiritoriEvents.TimerCountDown:
                counts.append(data['timer'])
                self.assertEqual(data['type'], ShiritoriEvents.TimerCountDown)
            elif data['type'] == ShiritoriEvents.TimerFinished:
                break
        self.assertEqual(len(counts), 4)
        # Close
        await communicator.disconnect()
