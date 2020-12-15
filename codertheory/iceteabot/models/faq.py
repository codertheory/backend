from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "FAQ",
)


class FAQ(BaseModel):
    guild = models.ForeignKey("DiscordGuild", on_delete=models.DO_NOTHING)
    author = models.ForeignKey("DiscordUser", on_delete=models.DO_NOTHING)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uses = models.IntegerField(default=0)
