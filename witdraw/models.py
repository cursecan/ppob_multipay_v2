from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase


class Witdraw(CommonBase):
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='witdraw_user', default=1)
    
    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return str(self.amount)