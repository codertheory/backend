from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".herokuapp.com", "staging.codertheory.dev"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}
# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": env.cache("REDIS_URL")
}

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ['whitenoise']
MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="codertheory <noreply@codertheory.com>"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[codertheory]"
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin")

# Anymail (Mailgun)
# ------------------------------------------------------------------------------

# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
if env("MAILGUN_API_KEY", default=None):
    # https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
    INSTALLED_APPS += ["anymail"]  # noqa F405
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
        "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
    }
# Your stuff...
# ------------------------------------------------------------------------------
CORS_ORIGIN_WHITELIST += [
    "https://polls.codertheory.dev"
    "https://polls-a6yh67nyt-lucascodert.vercel.app",
    "https://codertheory-shiritori.herokuapp.com",
]
