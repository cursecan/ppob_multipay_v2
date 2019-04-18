from django.apps import AppConfig


class BankreconConfig(AppConfig):
    name = 'bankrecon'

    def ready(self):
        from . import signals