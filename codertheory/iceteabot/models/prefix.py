from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "CommandPrefix",
)


class CommandPrefix(BaseModel):
    prefix = models.CharField(max_length=25)
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
