from django.db import models

from codertheory.iceteabot.models.base import DiscordModel

__all__ = (
    "CommandCall",
)


class CommandCall(DiscordModel):
    command = models.CharField(max_length=100)
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    author = models.ForeignKey("DiscordUser", on_delete=models.DO_NOTHING)
    called_at = models.DateTimeField(auto_now_add=True)
    prefix = models.ForeignKey("CommandPrefix", on_delete=models.DO_NOTHING)
