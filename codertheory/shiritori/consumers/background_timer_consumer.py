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

    async def _task(self, game_id):
        current_player_id = None
        is_finished = False
        while not is_finished:
            game = await self.get_game(game_id)
            for time_left in range(game.timer, -1, -1):
                game = await self.get_game(game_id)
                if game.current_player_id != current_player_id:
                    current_player_id = game.current_player_id
                    break
                if not game.is_finished:
                    await self.channel_layer.send(
                        f"{game_id}-timer",
                        {
                            "type": to_camel_case(str(ShiritoriEvents.TimerCountDown)),
                            "data": {
                                "timer": time_left
                            }
                        }
                    )
                    await asyncio.sleep(1)
                else:
                    is_finished = True
                    break
            await self.channel_layer.send(
                f"{game_id}-timer",
                {
                    "type": to_camel_case(str(ShiritoriEvents.TimerFinished))
                }
            )
            await asyncio.sleep(1.5)

    async def start(self, event: dict):
        game_id = event.get('game_id')
        if game_id:
            task = self.game_timers.get(game_id)
            if task:
                return
            else:
                self.game_timers[game_id] = asyncio.create_task(self._task(game_id))

    async def finish(self, event: dict):
        game_id = event.get('game_id')
        if game_id:
            task = self.game_timers.get(game_id)
            if task:
                task.cancel()
