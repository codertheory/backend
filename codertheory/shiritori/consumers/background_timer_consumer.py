import asyncio
import typing

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from graphene.utils.str_converters import to_camel_case

from codertheory.shiritori import models

__all__ = (
    "BackGroundTimerConsumer",
)

from codertheory.shiritori.events import ShiritoriEvents


class BackGroundTimerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(BackGroundTimerConsumer, self).__init__(*args, **kwargs)
        self.game_timers: typing.Dict[str, asyncio.Task] = {}

    @database_sync_to_async
    def get_game(self, game_id) -> typing.Awaitable[models.ShiritoriGame]:
        return models.ShiritoriGame.objects.get(pk=game_id)

    @database_sync_to_async
    def finish_game(self, game: models.ShiritoriGame) -> typing.Awaitable[None]:
        return game.finish()

    @database_sync_to_async
    def take_turn(self, game: models.ShiritoriGame) -> typing.Awaitable[None]:
        return game.take_turn(raise_exception=False)

    async def send_json(self, content, close=False):
        if "type" not in content:
            if isinstance(content, dict):
                content['type'] = ShiritoriEvents.Unknown
        data = {
            "type": to_camel_case(content.pop('type', ShiritoriEvents.Unknown)),
            "data": content
        }
        return await super(BackGroundTimerConsumer, self).send_json(data, close)

    async def _task(self, game_id):
        try:
            game = await self.get_game(game_id)
            for time_left in range(game.timer, -1, -1):
                await self.channel_layer.group_send(
                    f"{game_id}",
                    {
                        "type": ShiritoriEvents.TimerCountDown.value,
                        "data": {
                            "timer": time_left
                        }
                    }
                )
                await asyncio.sleep(1)
            await self.take_turn(game)
            await asyncio.sleep(1.5)
        except Exception as error:
            print(f"Error: {error}")

    def _start_task(self, game_id):
        task = self.game_timers.get(game_id)
        if task:
            return
        else:
            self.game_timers[game_id] = asyncio.create_task(self._task(game_id))

    def _cancel_task(self, game_id):
        task = self.game_timers.pop(game_id, None)
        if task:
            task.cancel()

    def _restart_task(self, game_id):
        self._cancel_task(game_id)
        self._start_task(game_id)

    async def game_started(self, event: dict):
        game_id = event.get('game_id')
        if game_id:
            self._start_task(game_id)

    async def game_finished(self, event: dict):
        game_id = event.get('game_id')
        if game_id:
            self._cancel_task(game_id)

    async def turn_taken(self, event: dict):
        game_id = event.get('game_id')
        if game_id:
            self._restart_task(game_id)
