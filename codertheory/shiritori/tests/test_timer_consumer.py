import asyncio
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
        game = GameFactory(timer=3, started=True)
        PlayerFactory.create_batch(2, game=game)
        return game

    async def _setup(self) -> typing.Tuple[WebsocketCommunicator, ShiritoriGame]:
        game = await self._create_game()
        communicator = WebsocketCommunicator(router, f"ws/shiritori/game/{game.id}/timer")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        return communicator, game

    async def test_countdown(self):
        communicator, game = await self._setup()
        counts = []
        while True:
            data = await communicator.receive_json_from(timeout=1.2)
            if data['type'] == ShiritoriEvents.TimerCountDown:
                counts.append(data['data']['timer'])
                self.assertEqual(data['type'], ShiritoriEvents.TimerCountDown)
            elif data['type'] == ShiritoriEvents.TimerFinished:
                break
        self.assertEqual(len(counts), 5)
        # Close
        await communicator.disconnect()

    async def test_reconnect_shows_accurate_time(self):
        communicator, game = await self._setup()
        await asyncio.sleep(1)
        await communicator.receive_json_from()

        # Close
        await communicator.disconnect()

        await asyncio.sleep(1)
        communicator = WebsocketCommunicator(router, f"ws/shiritori/game/{game.id}/timer")
        await communicator.connect()
        payload = await communicator.receive_json_from()
        self.assertLessEqual(payload['data']['timer'], 1)
        await communicator.disconnect()
