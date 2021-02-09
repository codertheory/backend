from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.api.serializers import *
from codertheory.shiritori.events import ShiritoriEvents


def send_data_to_channel(name: str, data: dict):
    data['type'] = str(data['type'])
    channel_layer = get_channel_layer()
    coro = async_to_sync(channel_layer.group_send)
    coro(name, data)


@receiver(signals.post_save, sender=models.ShiritoriGame)
def on_game_save(sender: type, instance: models.ShiritoriGame, created: bool, **kwargs):
    if created:
        # noinspection PyTypeChecker
        data = {
            "type": ShiritoriEvents.GameCreated,
        }
    elif instance.started:
        data = {
            "type": ShiritoriEvents.GameStarted,
            "game": instance.id
        }
    else:
        data = {
            "type": ShiritoriEvents.GameUpdated,
            "game": GameSerializer(instance).data
        }
    send_data_to_channel("lobby", data)
    send_data_to_channel(instance.id, data)


@receiver(signals.post_delete, sender=models.ShiritoriGame)
def on_game_delete(sender: type, instance: models.ShiritoriGame, using: str, **kwargs):
    data = {
        "type": ShiritoriEvents.GameDeleted
    }
    send_data_to_channel('lobby', data)
    send_data_to_channel(instance.id, data)


@receiver(signals.post_save, sender=models.ShiritoriPlayer)
def on_player_save(sender: type, instance: models.ShiritoriPlayer, created: bool, **kwargs):
    data = {
        "player": PlayerSerializer(instance).data
    }
    if created:
        data['type'] = ShiritoriEvents.PlayerCreated
    else:
        data['type'] = ShiritoriEvents.PlayerUpdated
    send_data_to_channel(instance.game.id, data)


@receiver(signals.post_delete, sender=models.ShiritoriPlayer)
def on_player_delete(sender: type, instance: models.ShiritoriPlayer, using: str, **kwargs):
    data = {
        "player": PlayerSerializer(instance).data,
        "type": ShiritoriEvents.PlayerDeleted
    }
    send_data_to_channel(instance.game.id, data)


@receiver(signals.post_save, sender=models.ShiritoriGameWord)
def on_word_save(sender: type, instance: models.ShiritoriGameWord, created: bool, **kwargs):
    if created:
        data = {
            "type": ShiritoriEvents.TurnTaken,
            "player": instance.player_id,
            "word": instance.word,
        }
        send_data_to_channel(instance.game.id, data)
