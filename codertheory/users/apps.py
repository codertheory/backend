from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "codertheory.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import codertheory.users.signals  # noqa F401
        except ImportError:
            pass

        try:
            from djoser import utils
            from django.contrib.auth import login, user_logged_in
            from djoser.conf import settings
            from knox.models import AuthToken
            from collections import namedtuple

            authtoken = namedtuple("authtoken", ['token_key', 'expiry', 'user'])

            def login_user(request, user):
                instance, token = AuthToken.objects.create(user)
                if settings.CREATE_SESSION_ON_LOGIN:
                    login(request, user)
                else:
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                return authtoken(token, instance.expiry, instance.user)

            utils.login_user = login_user
        except ImportError:
            pass
