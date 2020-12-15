from django.db import models

__all__ = (
    "DiscordModel",
)


class DiscordModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        abstract = True
