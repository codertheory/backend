from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "Task",
)


class Task(BaseModel):
    author = models.ForeignKey("DiscordUser", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    finished = models.BooleanField(default=False)
