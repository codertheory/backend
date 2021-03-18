from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'codertheory.polls'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from codertheory.polls import signals
