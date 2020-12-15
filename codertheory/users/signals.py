from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from knox import models as knox_models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        knox_models.AuthToken.objects.create(user=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_auth_token(sender, instance, using, **kwargs):
    knox_models.AuthToken.objects.get(user=instance).delete()
