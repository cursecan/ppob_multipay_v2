from django.apps import AppConfig


class BillingConfig(AppConfig):
    name = 'billing'

    def ready(self):
        from . import signals