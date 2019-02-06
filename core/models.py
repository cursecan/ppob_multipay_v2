from django.db import models

# Create your models here.


class CommonBase(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True