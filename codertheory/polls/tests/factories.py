import factory

from codertheory.polls import models
from codertheory.general.generator import generate_id

__all__ = (
    "PollFactory",
    "PollOptionFactory",
    "PollVoteFactory",
)


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Poll
        django_get_or_create = ("id",)

    id = factory.LazyFunction(generate_id)


class PollOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PollOption
        django_get_or_create = ("poll",)

    poll = factory.SubFactory(PollFactory)
    option = factory.Faker("word")


class PollVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PollVote
        django_get_or_create = ("poll",)

    option = factory.SubFactory(PollOptionFactory)
