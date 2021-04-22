from django.db import models
from django.db.models import QuerySet

from codertheory.general.models import BaseModel


# Create your models here.


class Poll(BaseModel):
    name = models.CharField(max_length=1000)
    description = models.TextField(default=None, null=True, blank=True)

    class Meta:
        ordering = [
            "-created_at"
        ]

    @property
    def options(self) -> QuerySet["PollOption"]:
        return PollOption.objects.filter(poll=self)

    @property
    def total_vote_count(self) -> int:
        return PollVote.objects.filter(option__poll_id=self.id).count()

    @property
    def votes(self) -> QuerySet['PollVote']:
        return PollVote.objects.filter(option__poll_id=self.id)

    def get_option(self, option_id) -> "PollOption":
        return PollOption.objects.get(poll_id=self.id, id=option_id)

    def to_dict(self):
        from .graphql.serializers import PollSerializer
        return PollSerializer(instance=self).data


class PollOption(BaseModel):
    option = models.CharField(max_length=1000)
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["option", "poll"], name="unique_option")
        ]
        order_with_respect_to = "poll"

    def vote(self, request=None):
        poll_vote = PollVote(option=self)
        poll_vote.save()
        return poll_vote

    @property
    def vote_count(self):
        return PollVote.objects.filter(option=self).count()


class PollVote(BaseModel):
    option = models.ForeignKey("PollOption", on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "option"
