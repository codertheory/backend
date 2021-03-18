import asyncio
import typing

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from codertheory.shiritori import models

__all__ = (
    "TimerConsumer",
)


class TimerConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def get_game(self, game_id) -> typing.Awaitable[models.ShiritoriGame]:
        return models.ShiritoriGame.objects.get(pk=game_id)

    @database_sync_to_async
    def finish_game(self, game: models.ShiritoriGame) -> typing.Awaitable[None]:
        return game.finish()

    async def websocket_connect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_add(f"{game_id}-timer", self.channel_name)
        await super(TimerConsumer, self).websocket_connect(message)
        try:
            result = await asyncio.wait_for(self.channel_layer.receive(), 2)
            await self.send_json(result)
        except asyncio.TimeoutError:
            pass

    async def websocket_disconnect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_discard(f"{game_id}-timer", self.channel_name)
        await super(TimerConsumer, self).websocket_disconnect(message)
        game = await self.get_game(game_id)
        await self.finish_game(game)
