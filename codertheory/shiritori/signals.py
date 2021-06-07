from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.events import ShiritoriEvents
from codertheory.shiritori.graphql.serializers import *
from codertheory.utils.ws_utils import send_data_to_channel


@receiver(signals.post_delete, sender=models.ShiritoriGame)
def on_game_delete(instance: models.ShiritoriGame, using: str, **kwargs):
    data = {
        "type": ShiritoriEvents.GameDeleted,
        "game": GameSerializer(instance).data
    }
    send_data_to_channel(instance.id, data)
    send_data_to_channel("lobby", data)


@receiver(signals.post_save, sender=models.ShiritoriGame)
def on_game_create(instance: models.ShiritoriGame, created: bool, **kwargs):
    if created:
        data = {
            "game": GameSerializer(instance).data,
            "type": ShiritoriEvents.GameCreated
        }
        send_data_to_channel("lobby", data)
