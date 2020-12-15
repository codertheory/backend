import factory

__all__ = (
    "GroupFactory",
)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.Group"

    name = factory.Faker('name')
