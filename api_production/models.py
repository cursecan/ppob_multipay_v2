from django.db import models

from core.models import CommonBase


class ProductVersion(CommonBase):
    version = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.version
