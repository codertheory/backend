from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "ReactionRole",
)


class ReactionRole(BaseModel):
    message_id = models.BigIntegerField()
    emoji = models.CharField(max_length=100)
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    role_id = models.BigIntegerField()
