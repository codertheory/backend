from django.db.models import signals
from django.dispatch import receiver

from codertheory.shiritori import models
from codertheory.shiritori.graphql.subscriptions import GameSubscription, PlayerSubscription


def game_broadcast(instance: models.ShiritoriGame):
    GameSubscription.broadcast(group=instance.id, payload={"game_id": instance.id})


def player_broadcast(instance: models.ShiritoriGame):
    PlayerSubscription.broadcast(group=instance.id, payload={'game_id': instance.id})


@receiver(signals.post_delete, sender=models.ShiritoriGame)
def on_game_delete(instance: models.ShiritoriGame, **kwargs):
    game_broadcast(instance)


@receiver(signals.post_save, sender=models.ShiritoriGame)
def on_game_create(instance: models.ShiritoriGame, created: bool, **kwargs):
    game_broadcast(instance)


@receiver(signals.post_delete, sender=models.ShiritoriPlayer)
def on_player_delete(instance: models.ShiritoriPlayer, **kwargs):
    game_broadcast(instance.game)
    player_broadcast(instance.game)


@receiver(signals.post_save, sender=models.ShiritoriPlayer)
def on_player_create(instance: models.ShiritoriPlayer, created: bool, **kwargs):
    game_broadcast(instance.game)
    if created:
        player_broadcast(instance.game)
