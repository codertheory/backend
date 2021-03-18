from django.db.models import signals
from django.dispatch import receiver

from codertheory.polls import models
from codertheory.polls.api import serializers
from codertheory.polls.events import PollEvents
from codertheory.utils.ws_utils import send_data_to_channel


@receiver(signals.post_save, sender=models.Poll)
def on_poll_save(instance: models.Poll, created: bool, **kwargs):
    if created:
        data = {
            "type": PollEvents.PollCreated,
            "poll": serializers.PollSerializer(instance).data
        }
        send_data_to_channel(instance.id, data)


@receiver(signals.post_delete, sender=models.Poll)
def on_poll_delete(instance: models.Poll, **kwargs):
    data = {
        "type": PollEvents.PollDeleted,
        "poll": instance.id
    }
    send_data_to_channel(instance.id, data)


@receiver(signals.post_save, sender=models.PollVote)
def on_poll_vote(instance: models.PollVote, created: bool, **kwargs):
    if created:
        data = {
            "type": PollEvents.PollVote,
            "poll": serializers.PollSerializer(instance.option.poll).data
        }
        send_data_to_channel(instance.option.poll.id, data)
