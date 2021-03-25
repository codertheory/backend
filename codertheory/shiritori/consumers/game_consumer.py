import typing

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from graphene.utils.str_converters import to_camel_case
from rest_framework.utils.serializer_helpers import ReturnDict

from codertheory.shiritori import models
from codertheory.shiritori.api import serializers
from codertheory.shiritori.events import ShiritoriEvents

__all__ = (
    "GameConsumer",
)


def get_handler_name(message):
    """
    Looks at a message, checks it has a sensible type, and returns the
    handler name for that type.
    """
    # Check message looks OK
    if "type" not in message:
        raise ValueError(f"Incoming message has no 'type' attribute: message {message}")
    # Extract type and replace . with _
    handler_name = message["type"].replace(".", "_")
    if handler_name.startswith("_"):
        raise ValueError("Malformed type in message (leading underscore)")
    return handler_name


class GameConsumer(AsyncJsonWebsocketConsumer):

    async def dispatch(self, message):
        if "type" not in message:
            if "game" in message:
                message['type'] = str(ShiritoriEvents.GameUpdated.value)
                message['data'] = message.pop('game')
                print("reformated message:", message)
        return await super(GameConsumer, self).dispatch(message)

    @database_sync_to_async
    def get_game(self, game_id) -> typing.Awaitable[ReturnDict]:
        game = models.ShiritoriGame.objects.get(pk=game_id)
        return serializers.GameSerializer(game).data

    async def websocket_connect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_add(game_id, self.channel_name)
        await super(GameConsumer, self).websocket_connect(message)
        try:
            game_data = await self.get_game(game_id)
        except models.ShiritoriGame.DoesNotExist:
            game_data = None
        event_type = "connect" if game_data else "notFound"
        await self.send_json(
            {"type": event_type, "game": game_data})

    async def websocket_disconnect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_discard(game_id, self.channel_name)
        await super(GameConsumer, self).websocket_disconnect(message)

    async def send_json(self, content, close=False):
        if "type" not in content:
            if isinstance(content, dict):
                content['type'] = str(ShiritoriEvents.Unknown)
        data = {
            "type": to_camel_case(content.pop('type')),
            "data": content.pop('data', content)
        }
        return await super(GameConsumer, self).send_json(data, close)

    async def game_updated(self, event: dict):
        if "game_id" in event:
            await self.send_json({
                "type": str(ShiritoriEvents.GameUpdated),
                "data": {
                    "game": await self.get_game(event.get('game_id'))
                }
            })
        else:
            await self.send_json(event)

    async def game_started(self, event: dict):
        await self.send_json(event)

    async def game_deleted(self, event: dict):
        await self.send_json(event)

    async def game_finished(self, event: dict):
        await self.send_json(event)

    async def player_created(self, event: dict):
        await self.send_json(event)

    async def player_updated(self, event: dict):
        await self.send_json(event)

    async def player_deleted(self, event: dict):
        await self.send_json(event)

    async def turn_taken(self, event: dict):
        try:
            game_data = await self.get_game(event['game_id'])
        except models.ShiritoriGame.DoesNotExist:
            game_data = None
        await self.send_json({
            "type": str(ShiritoriEvents.TurnTaken),
            "data": {
                "game": game_data
            }
        })

    async def timer_count_down(self, event: dict):
        await self.send_json({
            "type": str(ShiritoriEvents.TimerCountDown),
            "data": event['data']
        })
