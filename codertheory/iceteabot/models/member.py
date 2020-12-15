from django.db import models

from codertheory.iceteabot.models.base import DiscordModel

__all__ = (
    "DiscordMember",
)


class DiscordMember(DiscordModel):
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    administrator = models.BooleanField(default=False)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('id', 'guild'), name="unique_member"),
        )
