from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.api import serializers


@receiver(signals.post_save, sender=models.ShiritoriGame)
def on_game_save(sender: type, instance: models.ShiritoriGame, created: bool, **kwargs):
    channel_layer = get_channel_layer()
    coro = async_to_sync(channel_layer.group_send)
    data = {}
    if created:
        # noinspection PyTypeChecker
        data = {
            "type": "game_created",
            "game": serializers.GameSerializer(instance).data
        }
    elif instance.started:
        data = {
            "type": "game_started",
            "game": instance.id
        }
    coro('lobby', data)


@receiver(signals.post_save, sender=models.ShiritoriPlayer)
def on_player_save(sender: type, instance: models.ShiritoriPlayer, created: bool, **kwargs):
    pass
