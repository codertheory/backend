import asyncio

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from codertheory.shiritori.events import ShiritoriEvents
from codertheory.shiritori.tests import factories
from config.websocket import router


class LobbyConsumerTests(TransactionTestCase):
    serialized_rollback = False

    @database_sync_to_async
    def _create_games(self, amount: int = 5):
        return factories.GameFactory.create_batch(amount)

    @database_sync_to_async
    def save_game(self, g: factories.models.ShiritoriGame):
        g.start(ignore_count=True)

    async def _setUpData(self):
        communicator = WebsocketCommunicator(router, "ws/shiritori/lobby")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def test_on_connect(self):
        games = await self._create_games()
        communicator = await self._setUpData()
        # Test Receiving
        response = await communicator.receive_json_from()
        data = response['data']['games']
        self.assertEqual(len(data), len(games))
        # Close
        await communicator.disconnect()

    async def test_on_game_created(self):
        communicator = await self._setUpData()
        await asyncio.sleep(1)
        response = await communicator.receive_json_from()
        data = response['data']['games']
        self.assertEqual(len(data), 0)
        new_game = await self._create_games(1)
        new_response = await communicator.receive_json_from()
        data = new_response['data']['games']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], new_game[0].id)
        await communicator.disconnect()

    async def test_on_game_started(self):
        communicator = await self._setUpData()
        await communicator.receive_json_from()
        await asyncio.sleep(1)
        games = await self._create_games(1)
        await asyncio.sleep(1)
        await communicator.receive_json_from()

        await self.save_game(games[0])
        new_response = await communicator.receive_json_from()
        self.assertEqual(new_response['type'], ShiritoriEvents.GameStarted)
        data = new_response['data']
        self.assertEqual(data['id'], games[0].id)
        await communicator.disconnect()
