import factory

from codertheory.general.generator import generate_id
from codertheory.shiritori import models


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriGame
        django_get_or_create = ("id",)

    id = factory.LazyFunction(generate_id)
    last_word = "bar"

    # noinspection PyUnusedLocal
    @factory.post_generation
    def handle_start(self: models.ShiritoriGame, **kwargs):
        if self.started and self.players:
            # noinspection PyAttributeOutsideInit
            self.current_player = self.players[0]


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriPlayer
        django_get_or_create = ("name", "game")

    name = factory.Faker("name")
    score = 100
    game = factory.SubFactory(GameFactory)


class GameWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ShiritoriGameWord
        django_get_or_create = ("word", "game", "player")

    word = factory.Faker("word")
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)
