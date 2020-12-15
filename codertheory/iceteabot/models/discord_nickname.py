from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "DiscordNickName",
)


class DiscordNickName(BaseModel):
    name = models.TextField()
    member = models.ForeignKey("DiscordUser", on_delete=models.DO_NOTHING)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
