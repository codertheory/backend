from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from . import factories
from ..consumers import LobbyConsumer


class LobbyConsumerTests(TransactionTestCase):
    serialized_rollback = False

    @database_sync_to_async
    def create_games(self):
        return factories.GameFactory.create_batch(5)

    @database_sync_to_async
    def create_public_game(self):
        return factories.GameFactory(started=False)

    async def setUpData(self):
        communicator = WebsocketCommunicator(LobbyConsumer.as_asgi(), "ws/shiritori/lobby")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def test_on_connect_message(self):
        games = await self.create_games()
        communicator = await self.setUpData()
        # Test Receiving
        response = await communicator.receive_json_from()
        self.assertEqual(len(response), len(games))
        # Close
        await communicator.disconnect()

    async def test_on_new_game_created(self):
        communicator = await self.setUpData()
        response = await communicator.receive_json_from()
        self.assertEqual(len(response), 0)
        new_game = await self.create_public_game()
        new_response = await communicator.receive_json_from()
        self.assertEqual(len(new_response), 1)
        self.assertEqual(new_response[0]['id'], new_game.id)

    async def test_on_game_started(self):
        communicator = await self.setUpData()
        await communicator.receive_json_from()
