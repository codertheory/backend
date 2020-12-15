from django.apps import AppConfig


class ShiritoriConfig(AppConfig):
    name = 'codertheory.shiritori'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from codertheory.shiritori import signals
