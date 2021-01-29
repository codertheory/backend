from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "Activity",
)


class Activity(BaseModel):
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    status = models.TextField()
    role = models.BigIntegerField()

    class Meta:
        verbose_name_plural = "Activities"
