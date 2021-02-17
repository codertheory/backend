from channels.generic.websocket import JsonWebsocketConsumer
from graphene.utils.str_converters import to_camel_case

from codertheory.shiritori import models
from codertheory.shiritori.api import serializers
from codertheory.shiritori.events import ShiritoriEvents

__all__ = (
    "LobbyConsumer",
)


class LobbyConsumer(JsonWebsocketConsumer):
    groups = ['lobby']

    def websocket_connect(self, message):
        super(LobbyConsumer, self).websocket_connect(message)
        self._send_public_games(ShiritoriEvents.LobbyCreated.value)

    def _send_public_games(self, type: str):
        games = models.ShiritoriGame.objects.filter(started=False)
        games_data = serializers.GameSerializer(games, many=True)
        self.send_json({
            "type": to_camel_case(type),
            "data": {"games": games_data.data}
        })

    def game_created(self, event):
        self._send_public_games(event['type'])

    def game_deleted(self, event):
        self._send_public_games(event['type'])

    def game_started(self, event):
        self.send_json({
            "type": event['type'],
            "data": event['game']
        })
