from django.db import models

from codertheory.iceteabot.models.base import DiscordModel

__all__ = (
    "DiscordUser",
)


class DiscordUser(DiscordModel):
    blocked = models.BooleanField(default=False)
