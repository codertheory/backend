import factory.fuzzy
from django.utils import timezone
from pinax.blog import models

__all__ = (
    "SectionFactory",
    "ImageSetFactory",
    "PostFactory",
)

from codertheory.users.tests.factories import UserFactory


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.Faker("name")
    slug = factory.Faker("slug")


class ImageSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ImageSet

    created_by = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    title = factory.Faker("name")
    slug = factory.Faker("slug")
    secret_key = factory.Faker("password", length=8)
    markup = "markdown"
    section = factory.SubFactory(SectionFactory)
    author = factory.SubFactory(UserFactory)
    image_set = factory.SubFactory(ImageSetFactory)
    state = factory.fuzzy.FuzzyChoice([1, 2])
    published = factory.LazyFunction(timezone.now)
    blog_id = 1
