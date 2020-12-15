from allauth.account import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_verified_user(email, password, superuser: bool = True):
    if superuser:
        user = User.objects.create_superuser(None, email, password)
    else:
        user = User.objects.create_user(None, email, password)
    email_model = models.EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    models.EmailConfirmation.objects.create(email_address=email_model)
    return user
