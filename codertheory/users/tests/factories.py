from typing import Any, Sequence

import factory
from allauth.account import models as allauth_models
from django.contrib.auth import get_user_model
from factory import django
from rest_framework.authtoken import models as rest_framework_authtoken_models

class UserFactory(django.DjangoModelFactory):
    email = factory.Faker("email")
    name = factory.Faker("name")

    # noinspection PyUnresolvedReferences
    @factory.post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = factory.Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).evaluate(None, None, dict(locale="en_US"))
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]

    @factory.post_generation
    def verify_email(self, create: bool, extracted: Sequence[Any], **kwargs):
        if not create:
            return
        email = EmailAddressFactory(user=self)
        EmailAddressConfirmationFactory(email_address=email)


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class EmailAddressFactory(django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    email = factory.LazyAttribute(lambda self: self.user.email)
    verified = True
    primary = True

    class Meta:
        model = allauth_models.EmailAddress
        django_get_or_create = ("user", "email")


class EmailAddressConfirmationFactory(django.DjangoModelFactory):
    email_address = factory.SubFactory(EmailAddressFactory)
    key = factory.Faker('iban')

    class Meta:
        model = allauth_models.EmailConfirmation
        django_get_or_create = ('email_address', 'key')


class DRFTokenFactory(django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = rest_framework_authtoken_models.Token
        django_get_or_create = ('user',)
