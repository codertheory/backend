from django.db import models

from codertheory.general.models import BaseModel

__all__ = (
    "Tag",
    "TagLookUp",
    "TagCall",
)


class TagBase(BaseModel):
    name = models.CharField(max_length=120)
    author = models.ForeignKey("DiscordUser", on_delete=models.SET_NULL, null=True)
    guild = models.ForeignKey("DiscordGuild", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Tag(TagBase):
    content = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True)


class TagLookUp(TagBase):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)


class TagCall(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    channel = models.ForeignKey("DiscordChannel", on_delete=models.CASCADE)
    called_at = models.DateTimeField(auto_now_add=True)
