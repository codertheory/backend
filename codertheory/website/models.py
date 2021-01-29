from colorfield.fields import ColorField
from django.db import models

__all__ = (
    "BannerButton",
    "BannerImage",
    "DisplayBanner",
)


class BannerButton(models.Model):
    text = models.CharField(max_length=15)
    background_color = ColorField()
    text_color = ColorField()


class BannerImage(models.Model):
    image = models.ImageField()


class DisplayBanner(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    image = models.ForeignKey(BannerImage, blank=True, null=True, on_delete=models.SET_NULL)
    primary_button = models.ForeignKey(BannerButton, blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    secondary_button = models.ForeignKey(BannerButton, blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=False)
