import factory

from codertheory.shiritori import models
from codertheory.utils.generator import generate_id


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriGame
        django_get_or_create = ("id",)

    id = factory.LazyFunction(lambda: generate_id())
    last_word = "bar"


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriPlayer
        django_get_or_create = ("name", "game")

    name = factory.Faker("name")
    score = 100
    game = factory.SubFactory(GameFactory)
    lives = 3


class GameWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriGameWord
        django_get_or_create = ("word", "game", "player")

    word = factory.Faker("word")
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)
