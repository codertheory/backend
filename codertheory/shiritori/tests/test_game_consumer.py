import typing

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from codertheory.shiritori.events import ShiritoriEvents
from codertheory.shiritori.factories import *
from codertheory.shiritori.models import *
from config.websocket import router


class GameConsumerTests(TransactionTestCase):
    serialized_rollback = False

    @database_sync_to_async
    def _create_game(self) -> typing.Awaitable[ShiritoriGame]:
        return GameFactory()

    @database_sync_to_async
    def _start_game(self, g):
        g.started = True
        g.save()

    @database_sync_to_async
    def _join_game(self, g) -> typing.Awaitable[ShiritoriPlayer]:
        return PlayerFactory(game=g)

    @database_sync_to_async
    def _update_player(self, p: ShiritoriPlayer):
        p.name = "snowmaker"
        p.save()

    @database_sync_to_async
    def _leave_game(self, p: ShiritoriPlayer):
        p.delete()

    @database_sync_to_async
    def _take_turn(self, p: ShiritoriPlayer) -> typing.Awaitable[ShiritoriGameWord]:
        return GameWordFactory(player=p, game=p.game)

    async def _setup(self) -> typing.Tuple[WebsocketCommunicator, ShiritoriGame]:
        game = await self._create_game()
        communicator = WebsocketCommunicator(router, f"ws/shiritori/game/{game.id}")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_json_from()
        return communicator, game

    async def test_on_game_start(self):
        communicator, game = await self._setup()
        await self._start_game(game)
        data = await communicator.receive_json_from()
        self.assertEqual(data['type'], ShiritoriEvents.GameStarted.value)
        # Close
        await communicator.disconnect()

    async def test_on_player_created(self):
        communicator, game = await self._setup()
        player = await self._join_game(game)
        data = await communicator.receive_json_from()
        self.assertEqual(data['type'], ShiritoriEvents.PlayerCreated.value)
        self.assertEqual(data['data']['player']['id'], player.id)
        # Close
        await communicator.disconnect()

    async def test_on_player_updated(self):
        communicator, game = await self._setup()
        player = await self._join_game(game)
        await communicator.receive_json_from()
        await self._update_player(player)
        data = await communicator.receive_json_from()
        self.assertEqual(data['type'], ShiritoriEvents.PlayerUpdated.value)
        self.assertEqual(data['data']['player']['id'], player.id)

        # Close
        await communicator.disconnect()

    async def test_on_player_left(self):
        communicator, game = await self._setup()
        player = await self._join_game(game)
        player_id = str(player.id)
        await communicator.receive_json_from()
        await self._leave_game(player)
        data = await communicator.receive_json_from()
        self.assertEqual(data['type'], ShiritoriEvents.PlayerDeleted.value)
        self.assertEqual(data['data']['player']['id'], player_id)

        # Close
        await communicator.disconnect()

    async def test_on_turn_taken(self):
        communicator, game = await self._setup()
        player = await self._join_game(game)
        await communicator.receive_json_from()
        word = await self._take_turn(player)
        data = await communicator.receive_json_from()
        self.assertEqual(data['type'], ShiritoriEvents.TurnTaken.value)
        self.assertEqual(data['data']['player'], player.id)
        self.assertEqual(data['data']['word'], word.word)
        # Close
        await communicator.disconnect()
