from codertheory.shiritori.events import ShiritoriEvents
from codertheory.utils.ws_utils import send_data_to_channel

__all__ = (
    "send_start_game_event",
    "send_finish_game_event"
)


def send_game_event(game, event):
    from codertheory.shiritori.api import serializers
    data = {
        "game": serializers.GameSerializer(game).data,
        "type": event
    }
    send_data_to_channel("lobby", data)
    send_data_to_channel(game.id, data)


def send_start_game_event(game):
    send_game_event(game, ShiritoriEvents.GameStarted)
    send_data_to_channel("timer", {
        "type": "start",
        "game_id": game.id
    })


def send_finish_game_event(game):
    send_game_event(game, ShiritoriEvents.GameFinished)
    send_data_to_channel("timer", {
        "type": "finish",
        "game_id": game.id
    })
