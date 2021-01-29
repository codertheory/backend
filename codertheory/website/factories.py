import factory
from factory import django

from codertheory.website.models import *

__all__ = (
    "BannerButtonFactory",
    "BannerImageFactory",
    "DisplayBannerFactory",
)


class BannerButtonFactory(django.DjangoModelFactory):
    class Meta:
        model = BannerButton
        django_get_or_create = ("text",)

    text = factory.Faker("text")
    background_color = factory.Faker("hex_color")
    text_color = factory.Faker("hex_color")


class BannerImageFactory(django.DjangoModelFactory):
    class Meta:
        model = BannerImage
        django_get_or_create = ('name',)

    name = factory.Faker("name")
    image = django.ImageField()


class DisplayBannerFactory(django.DjangoModelFactory):
    class Meta:
        model = DisplayBanner
        django_get_or_create = ("title", "description")

    title = factory.Faker("text")
    description = factory.Faker("text")
    image = django.ImageField()
    primary_button = factory.SubFactory(BannerButtonFactory)
    secondary_button = factory.SubFactory(BannerButtonFactory)
