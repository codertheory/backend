from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "Reminder",
)


class Reminder(BaseModel):
    user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)
    message = models.CharField(max_length=1500)
    channel = models.ForeignKey("DiscordChannel", on_delete=models.CASCADE)
    event = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
