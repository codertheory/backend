from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.graphql.subscriptions import GameSubscription


def broadcast(instance):
    GameSubscription.broadcast(group=instance.id, payload={"game_id": instance.id})


@receiver(signals.post_delete, sender=models.ShiritoriGame)
def on_game_delete(instance: models.ShiritoriGame, **kwargs):
    broadcast(instance)


@receiver(signals.post_save, sender=models.ShiritoriGame)
def on_game_create(instance: models.ShiritoriGame, created: bool, **kwargs):
    broadcast(instance)


@receiver(signals.post_delete, sender=models.ShiritoriPlayer)
def on_player_delete(instance: models.ShiritoriPlayer, **kwargs):
    broadcast(instance.game)


@receiver(signals.post_save, sender=models.ShiritoriPlayer)
def on_player_create(instance: models.ShiritoriPlayer, **kwargs):
    broadcast(instance.game)
