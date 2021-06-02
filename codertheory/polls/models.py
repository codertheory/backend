import ipinfo
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet, Count

from codertheory.general.models import BaseModel


# Create your models here.


class Poll(BaseModel):
    name = models.CharField(max_length=1000)
    description = models.TextField(default=None, null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "-created_at"
        ]

    @property
    def options(self) -> QuerySet["PollOption"]:
        return PollOption.objects.filter(poll=self)

    @property
    def total_vote_count(self) -> int:
        return PollVote.objects.filter(poll_id=self.id).count()

    @property
    def votes(self) -> QuerySet['PollVote']:
        return PollVote.objects.filter(poll_id=self.id)

    def get_option(self, option_id) -> "PollOption":
        return PollOption.objects.get(poll_id=self.id, id=option_id)

    def to_dict(self):
        from .graphql.serializers import PollSerializer
        return PollSerializer(instance=self).data

    @staticmethod
    def can_vote(poll_id, ip):
        return not PollVote.objects.filter(poll_id=poll_id, ip=ip).exists()


class PollOption(BaseModel):
    option = models.CharField(max_length=1000)
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["option", "poll"], name="unique_option")
        ]
        order_with_respect_to = "poll"

    @property
    def vote_count(self):
        return PollVote.objects.filter(option=self).count()

    @property
    def vote_percentage(self):
        option_vote_count = Count("option", filter=Q(option_id=self.id), output_field=models.FloatField())
        total_vote_count = Count("poll", filter=Q(poll_id=self.poll.id), output_field=models.FloatField())
        result = PollVote.objects.aggregate(total_vote_count=total_vote_count, vote_count=option_vote_count)
        if result['total_vote_count'] > 0 and result['vote_count'] > 0:
            return result['vote_count'] / result['total_vote_count']
        else:
            return 0


class PollVote(BaseModel):
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE)
    option = models.ForeignKey("PollOption", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        order_with_respect_to = "option"
        constraints = [
            models.UniqueConstraint(
                fields=["poll", "ip"],
                name="Unique IP Per Poll"
            )
        ]

    @classmethod
    def vote(cls, poll_id: str, option_id: str, ip: str, **kwargs) -> "PollVote":
        try:
            handler = ipinfo.getHandler(settings.IPINFO_API_KEY)
            details = handler.getDetails(ip)
            metadata = {
                "city": details.city,
                "region": details.region,
                "country": details.country
            }
        except Exception:
            metadata = {}
        return PollVote.objects.create(poll_id=poll_id, option_id=option_id, ip=ip, metadata=metadata)
