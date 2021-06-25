from django.db.models import signals
from django.dispatch import receiver

from codertheory.polls import models
from codertheory.polls.graphql.subscriptions import PollSubscription


@receiver(signals.post_save, sender=models.Poll)
def on_poll_save(instance: models.Poll, created: bool, **kwargs):
    if created:
        PollSubscription.broadcast(group=instance.id, payload={"poll": {"id": instance.id}})


@receiver(signals.post_delete, sender=models.Poll)
def on_poll_delete(instance: models.Poll, **kwargs):
    PollSubscription.broadcast(group=instance.id, payload={"poll": {"id": instance.id}})


@receiver(signals.post_save, sender=models.PollVote)
def on_poll_vote(instance: models.PollVote, created: bool, **kwargs):
    PollSubscription.broadcast(group=instance.poll.id, payload={"poll": {"id": instance.poll.id}})


@receiver(signals.post_delete, sender=models.PollVote)
def on_vote_delete(instance: models.PollVote, **kwargs):
    PollSubscription.broadcast(group=instance.poll.id, payload={"poll": {"id": instance.poll.id}})
