from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from core.models import CommonBase

import uuid

class Profile(CommonBase):
    MEMBER = 1
    AGEN = 2
    PERSONAL = 3
    PROFILE_TYPE_LIST = (
        (MEMBER, 'MEMBER'),
        (AGEN, 'AGEN'),
        (PERSONAL, 'PERSONAL')
    )
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ponsel = models.CharField(max_length=20, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=PROFILE_TYPE_LIST, default=PERSONAL)
    agen = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile_agen')
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_agen(self):
        return self.agen.username

    def get_fullname(self):
        return self.user.first_name + ' ' + self.user.last_name


class Wallet(CommonBase):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.profile.user.username

    def get_saldo(self):
        if self.saldo < 0:
            return 0
        return self.saldo