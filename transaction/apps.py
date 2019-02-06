from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'transaction'

    def ready(self):
        from . import signals