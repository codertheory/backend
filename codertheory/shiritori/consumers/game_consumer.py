from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

__all__ = (
    "GameConsumer",
)


class GameConsumer(JsonWebsocketConsumer):

    def websocket_connect(self, message):
        game = self.scope['url_route']['kwargs']['game']
        async_to_sync(self.channel_layer.group_add)(game, self.channel_name)
        super(GameConsumer, self).websocket_connect(message)

    def websocket_disconnect(self, message):
        game = self.scope['url_route']['kwargs']['game']
        async_to_sync(self.channel_layer.group_discard)(game, self.channel_name)
        super(GameConsumer, self).websocket_disconnect(message)

    def send_json(self, content, close=False):
        data = {
            "type": content.pop('type'),
            "data": content
        }
        return super(GameConsumer, self).send_json(data, close)

    def game_updated(self, event: dict):
        self.send_json(event)

    def game_started(self, event: dict):
        self.send_json(event)

    def game_deleted(self, event: dict):
        self.send_json(event)

    def game_finished(self, event: dict):
        self.send_json(event)

    def player_created(self, event: dict):
        self.send_json(event)

    def player_updated(self, event: dict):
        self.send_json(event)

    def player_deleted(self, event: dict):
        self.send_json(event)

    def turn_taken(self, event: dict):
        self.send_json(event)
