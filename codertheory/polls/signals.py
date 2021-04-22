from django.db.models import signals
from django.dispatch import receiver

from codertheory.polls import models
from codertheory.polls.events import PollEvents
from codertheory.polls.graphql import serializers
from codertheory.polls.graphql.subscriptions import PollSubscription


@receiver(signals.post_save, sender=models.Poll)
def on_poll_save(instance: models.Poll, created: bool, **kwargs):
    if created:
        data = {
            "type": PollEvents.PollCreated.value,
            "poll": serializers.PollSerializer(instance).data
        }
        PollSubscription.broadcast(group=instance.id, payload=data)


@receiver(signals.post_delete, sender=models.Poll)
def on_poll_delete(instance: models.Poll, **kwargs):
    data = {
        "type": PollEvents.PollDeleted.value,
        "poll": instance.id
    }
    PollSubscription.broadcast(group=instance.id, payload=data)


@receiver(signals.post_save, sender=models.PollVote)
def on_poll_vote(instance: models.PollVote, created: bool, **kwargs):
    if created:
        data = {
            "type": PollEvents.PollVote.value,
            "poll": serializers.PollSerializer(instance.option.poll).data
        }
        PollSubscription.broadcast(group=instance.option.poll.id, payload=data)
