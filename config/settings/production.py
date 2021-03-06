from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["api.codertheory.dev", "codertheory-api.herokuapp.com"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
# DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}
# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": env.cache("REDIS_URL")
}

# SECURITY
# ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# # TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ['whitenoise']
MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA
# ------------------------------------------------------------------------------
# region http://stackoverflow.com/questions/10390244/
# Full-fledge class: https://stackoverflow.com/a/18046120/104731

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
    "DJANGO_DEFAULT_FROM_EMAIL", default="codertheory <noreply@codertheory.dev>"
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

# # Collectfast
# # ------------------------------------------------------------------------------
# # https://github.com/antonagestam/collectfast#installation
# INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS  # noqa F405
# COLLECTFAST_CACHE = 'collectfast'
# MAX_ENTRIES = 1000

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING['disable_existing_loggers'] = True
LOGGING['loggers'].update({
    "django.db.backends": {
        "level": "ERROR",
        "handlers": ["console"],
        "propagate": False,
    },
    # Errors logged by the SDK itself
    "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    "django.security.DisallowedHost": {
        "level": "ERROR",
        "handlers": ["console"],
        "propagate": False,
    },
})
# Your stuff...
# ------------------------------------------------------------------------------
ELASTICSEARCH_DSL['default']['use_ssl'] = True
CORS_ORIGIN_WHITELIST += [
    "https://shiritori.codertheory.dev",
    "https://polls.codertheory.dev",
    "https://shiritori-lucascodert.vercel.app",
    "https://codertheory-api.herokuapp.com",
]
