from unittest import skip

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TestCase

from . import factories


@skip
class LobbyConsumerTests(TestCase):

    @database_sync_to_async
    def setup_games(self):
        factories.GameFactory.create_batch(5)

    async def asyncSetUp(self):
        from config.ws_router import application
        self.communicator = WebsocketCommunicator(application, "ws/shiritori/lobby")
        await self.setup_games()

    async def asyncTearDown(self) -> None:
        await self.communicator.disconnect()

    async def test_receive_lobby_games_on_connect(self):
        await self.asyncSetUp()
        connected, subprotocol = await self.communicator.connect()
        assert connected is True
        response = await self.communicator.receive_json_from()
        self.assertGreaterEqual(len(response), 5)
        await self.asyncTearDown()

    async def test_receive_game_created(self):
        await self.asyncSetUp()
        connected, subprotocol = await self.communicator.connect()
        assert connected is True
        await self.communicator.receive_output()
        await self.communicator.send_input({
            "type": "game_created",
            "game": {"name": "New Game +"}
        })
        new_game = await self.communicator.receive_json_from(timeout=2)
        self.assertEqual(new_game['name'], "New Game +")
        await self.asyncTearDown()
