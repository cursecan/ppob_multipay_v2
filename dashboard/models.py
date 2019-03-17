from django.db import models

from core.models import CommonBase

class Application(CommonBase):
    app_name = models.CharField(max_length=100)
    attach = models.FileField(upload_to='application/')

    def __str__(self):
        return self.app_name
