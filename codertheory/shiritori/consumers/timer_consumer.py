import asyncio

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from graphene.utils.str_converters import to_camel_case

from codertheory.shiritori import models

__all__ = (
    "TimerConsumer",
)

from codertheory.shiritori.events import ShiritoriEvents


class TimerConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def get_game(self, game_id):
        return models.ShiritoriGame.objects.get(pk=game_id)

    async def websocket_connect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_add(f"{game_id}-timer", self.channel_name)
        await super(TimerConsumer, self).websocket_connect(message)
        game = await self.get_game(game_id)
        for time_left in range(game.seconds_until_expiration, -1, -1):
            if not game.is_timer_expired:
                await self.send_json({
                    "type": to_camel_case(str(ShiritoriEvents.TimerCountDown)),
                    "timer": time_left
                })
                await asyncio.sleep(0.75)
            else:
                break
        await self.send_json({
            "type": to_camel_case(str(ShiritoriEvents.TimerFinished))
        })

    async def websocket_disconnect(self, message):
        game_id = self.scope['url_route']['kwargs']['game']
        await self.channel_layer.group_discard(f"{game_id}-timer", self.channel_name)
        await super(TimerConsumer, self).websocket_disconnect(message)

