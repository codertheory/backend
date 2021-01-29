from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from codertheory.shiritori import models
from codertheory.shiritori.api import serializers

__all__ = (
    "LobbyConsumer",
)


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    groups = ['lobby']

    async def connect(self):
        await super(LobbyConsumer, self).connect()
        games = await self._get_public_games()
        await self.send_json(games)

    @database_sync_to_async
    def _get_public_games(self):
        games = models.ShiritoriGame.objects.filter(started=False)
        games_json = serializers.GameSerializer(games, many=True)
        return games_json.data

    async def game_created(self, event):
        await self.send_json(await self._get_public_games())

    async def game_started(self, event):
        pass
