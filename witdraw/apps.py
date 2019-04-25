from django.apps import AppConfig


class WitdrawConfig(AppConfig):
    name = 'witdraw'

    def ready(self):
        from . import signals