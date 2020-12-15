from django.db import models

from codertheory.iceteabot.models.base import DiscordModel

__all__ = (
    "DiscordChannel",
)


class DiscordChannel(DiscordModel):
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    blocked = models.BooleanField(default=False)
    blocked_reason = models.TextField(null=True, blank=True)
