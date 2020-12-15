from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from codertheory.shiritori import models
from codertheory.shiritori.api import serializers


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    groups = ['lobby']

    async def websocket_connect(self, message):
        await super(LobbyConsumer, self).websocket_connect(message)
        games = await self._get_public_games()
        await self.send_json(games)

    @database_sync_to_async
    def _get_public_games(self):
        games = models.ShiritoriGame.objects.filter(started=False)
        games_json = serializers.GameSerializer(games, many=True)
        return games_json.data

    async def game_created(self, event):
        await self.send_json(event['game'])

    async def game_started(self, event):
        pass
