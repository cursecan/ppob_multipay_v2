from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from core.models import CommonBase

import uuid, re

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
            'user__username'
        ]

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_agen(self):
        return self.agen.username

    def get_fullname(self):
        return self.user.first_name + ' ' + self.user.last_name

    def get_hidden_ponsel(self):
        try:
            return re.sub(r'\d{3}$', 'XXX', self.ponsel)
        except:
            return None

    def get_usertype(self):
        if not self.user.is_superuser:
            return self.get_user_type.display()
        return 'ADMIN'


class Wallet(CommonBase):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    commision = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    loan = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    limit = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    init_loan = models.DecimalField(max_digits=15, decimal_places=0, default=0)

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


class UploadUser(models.Model):
    username = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username