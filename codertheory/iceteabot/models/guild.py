from django.db import models

from codertheory.general.models import BaseModel
from codertheory.iceteabot.models.base import DiscordModel

__all__ = (
    "DiscordResponse",
    "DiscordGuild"
)


class DiscordResponse(BaseModel):
    content = models.TextField()
    channel = models.ForeignKey("DiscordChannel", on_delete=models.DO_NOTHING)
    author = models.ForeignKey("DiscordUser", on_delete=models.DO_NOTHING)
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)


class DiscordGuild(DiscordModel):
    tracking = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)
